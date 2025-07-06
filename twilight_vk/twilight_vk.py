from typing import Callable, List
import asyncio
from threading import Thread
from pathlib import Path

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from .components.logo import LogoComponent
from .logger.darky_logger import DarkyLogger
from .logger.darky_visual import Visual, STYLE, FG
from .utils.config_loader import Configuration
from .framework.handlers.exceptions import InitError
from .framework.bot_longpoll import BotsLongPoll
from .framework.api.api import VkBaseMethods
from .framework.api.methods import VkMethods

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

CONFIG = Configuration().get_config()

Visual.ansi()
   
class TwilightVK:

    def __init__(self, 
                 ACCESS_TOKEN:str=None, 
                 GROUP_ID:int=None, 
                 API_VERSION:str=CONFIG.vk_api.version) -> None:

        '''
        Initializes TwilightVK as module

        :param ACCESS_TOKEN: your group's access token, you can find it here(https://dev.vk.com/ru/api/access-token/community-token/in-community-settings)
        :type ACCESS_TOKEN: str

        :param GROUP_ID: your group's id, you can find it in your group's settings
        :type GROUP_ID: int

        :param API_VERSION: version of VK API, by default its grabbed from the frameworks's default configuration
        :type API_VERSION: str | None
        '''

        self.__access_token__ = ACCESS_TOKEN
        self.__group_id__ = GROUP_ID
        self.__api_version__ = API_VERSION
        
        self.__startup_callbacks__: List[Callable] = []
        self.__shutdown_callbacks__: List[Callable] = []

        self.__bot__ = BotsLongPoll(self.__access_token__,
                                    self.__group_id__,
                                    self.__api_version__)
        self.methods = None
        self.logo = LogoComponent()
        self.logger = DarkyLogger(logger_name=f"twilight-vk", configuration=CONFIG.LOGGER)

        if ACCESS_TOKEN == None:
            raise InitError("ACCESS_TOKEN is None!")
        
        if GROUP_ID == None:
            raise InitError("GROUP_ID is None!")
    
    def on_startup(self, func):
        self.__startup_callbacks__.append(func)
    
    def on_shutdown(self, func):
        self.__shutdown_callbacks__.append(func)
    
    @staticmethod
    async def __callback_func__(func):
        if asyncio.iscoroutinefunction(func):
            await func()
        else:
            func()

    async def run_polling(self):
        try:
            self.logger.info(f"Starting the TwilightVK framework...")
            for callback in self.__startup_callbacks__:
                await self.__callback_func__(callback)
            self.logger.info(f"{FG.BLUE}TwilightVK is started{STYLE.RESET}")
            await self.__bot__.auth()
            self.methods = await self.__bot__.get_vk_methods()
            async for event in self.__bot__.listen():
                ...
        except asyncio.CancelledError:
            self.logger.warning(f"Polling was forcibly canceled (it is not recommend to do this)")
            self.__bot__.stop()
        finally:
            for callback in self.__shutdown_callbacks__:
                await self.__callback_func__(callback)
            self.logger.info(f"{FG.RED}TwilightVK has been stopped!{STYLE.RESET}")
            self.__bot__.wait_for_response = False
            self.__bot__.__is_polling__ = False
        
    def start(self):
        try:
            self.logger.info(self.logo.colored)
            framework_task = asyncio.shield(asyncio.create_task(self.run_polling()))
            asyncio.run(asyncio.gather(framework_task))
        except KeyboardInterrupt:
            self.logger.info(f"KeyboardInterrupt recieved. Shutting down(to force press Ctrl+C again)...")
            self.__bot__.stop()
        except Exception as ex:
            self.logger.critical(f"Framework was crashed", exc_info=True)

    def stop(self):
        if self.__bot__.__is_polling__ or self.__bot__.wait_for_response:
            self.logger.debug(f"TwilightVK was asked to stop")
            self.__bot__.stop()
        else:
            self.logger.debug(f"TwilightVK was already stopped")


class TwilightAPI:

    def __init__(self,
                 HOST:str=CONFIG.api.host,
                 PORT:str=CONFIG.api.port,
                 FRAMEWORK:object=None):
        
        '''
        Initializes TwilightVK as separate API
        
        :param HOST: sets the host ip adress for API
        :type HOST: str

        :param PORT: sets the port for API
        :type PORT: str

        :param FRAMEWORK: Initialized and configured bot's framework
        :type FRAMEWORK: object | None
        '''

        self.__shutdown_initiated__ = False

        self.__startup_callbacks__: List[Callable] = []
        self.__shutdown_callbacks__: List[Callable] = []

        self.__HOST__ = HOST
        self.__PORT__ = PORT
        self.__api__ = FastAPI(
            title=CONFIG.api.title,
            description=CONFIG.api.description,
            version=CONFIG.api.version,
            lifespan=self.lifespan
            )
        self.__framework__ = FRAMEWORK

        self.__loop__ = asyncio.new_event_loop()

        self.__api_task__ = None
        self.__framework_task__ = None

        self.__router__ = APIRouter()
        self.__router__.add_api_route("/ping", self.ping, methods=["GET"], 
                                  tags=["API"], name=CONFIG.api.routes.ping.name,
                                  description=CONFIG.api.routes.ping.description)
        self.__router__.add_api_route("/stop", self.stop, methods=["GET"],
                                      tags=["API"], name=CONFIG.api.routes.stop.name,
                                      description=CONFIG.api.routes.stop.description)
        self.__router__.add_api_route("/favicon.ico", self.favicon, include_in_schema=False, methods=["GET"])

        self.__api__.include_router(self.__router__)

        self.logo = LogoComponent()
        self.logger = DarkyLogger(logger_name=f"twilight-api", configuration=CONFIG.LOGGER)

    def start(self):
        try:
            self.logger.info(self.logo.colored)
            self.logger.info(f"Starting...")
            self.__loop__.run_until_complete(self._run_threads())
        except KeyboardInterrupt:
            self.logger.warning(f"KeyboardInterrupt recieved, shutting down...")
            self.__loop__.run_until_complete(self.__shutdown_api__(force=True))
        except Exception as ex:
            self.logger.error(f"Error while starting: {ex}")
        finally:
            self.__loop__.run_until_complete(self.__loop__.shutdown_asyncgens())
            self.__loop__.close()

    async def _run_threads(self):
        try:
            uvicorn_config = uvicorn.Config(
                app=self.__api__,
                host=self.__HOST__,
                port=self.__PORT__,
                log_config=CONFIG.LOGGER
            )
            self.__uvicorn_server__ = uvicorn.Server(uvicorn_config)
            
            while self.__framework__ == None:
                pass
            
            self.__api_task__ = asyncio.shield(asyncio.create_task(self.__uvicorn_server__.serve()))
            self.__framework_task__ = asyncio.create_task(self.__framework__.run_polling())

            await asyncio.gather(
                self.__api_task__,
                self.__framework_task__,
                return_exceptions=True)
            
        except Exception as e:
            self.logger.error(f"Failed to start API: {e}")
            await self.__shutdown_api__()
    
    def on_startup(self, func):
        self.__startup_callbacks__.append(func)
    
    def on_shutdown(self, func):
        self.__shutdown_callbacks__.append(func)
    
    @staticmethod
    async def __callback_func__(func):
        if asyncio.iscoroutinefunction(func):
            await func()
        else:
            func()
    
    @asynccontextmanager
    async def lifespan(self, api: FastAPI):
        '''
        Provides start_up(preparing API wrapper) and
        shut_down(saving data for example) event handling
        '''
        try:
            '''Here is the startup code'''
            self.logger.info(f"Starting the Twilight API...")
            for callback in self.__startup_callbacks__:
                await self.__callback_func__(callback)
            if self.__framework__ == None:
                self.logger.warning(f"Framework was not configured!")
                self.logger.info(f"Initializing default TwilightVK...")
                self.__framework__ = TwilightVK("123", 123)
            self.logger.info(f"{FG.BLUE}Twilight API is started{STYLE.RESET} (on {CONFIG.api.host}:{CONFIG.api.port})")
            yield
            '''Here is the shutdown code'''
            for callback in self.__shutdown_callbacks__:
                await self.__callback_func__(callback)
            self.__uvicorn_server__.started = False
            self.logger.info(f"{FG.RED}Twilight API has been stopped{STYLE.RESET}")
        except Exception as e:
            self.logger.error(f"Error in API: {e}")
            await self.__shutdown_api__()

    async def get_api(self) -> FastAPI:
        return self.__api__
    
    async def ping(self) -> dict: #!ЭТО МЕТОД API
        return {"response": "pong"}
    
    async def stop(self, force:bool=False) -> dict: #!ЭТО МЕТОД API
        
        if not self.__shutdown_initiated__:
            self.__shutdown_initiated__ = True

        self.logger.info("Shutdown initiated!")
        await asyncio.create_task(self.__shutdown_api__(force=force))
        return {"response": "shutdown initiated!",
                "params": {
                    "force": force
                }}
    
    async def __shutdown_api__(self, force:bool=False):

        if self.__uvicorn_server__.started:
            self.logger.debug(f"Shutting down the API...")
            self.__uvicorn_server__.should_exit = True
            await asyncio.sleep(0.1)
        
        if self.__framework__:
            self.logger.debug(f"Shutting down the framework...")
            if force:
                self.__framework_task__.cancel()
            self.__framework__.stop()
    
    async def favicon(self) -> FileResponse: #!ЭТО МЕТОД API
        return FileResponse(ASSETS / "favicon.ico")