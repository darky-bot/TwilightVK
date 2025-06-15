from typing import Callable, List
import asyncio
from threading import Thread
from pathlib import Path

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from .logger.darky_logger import DarkyLogger
from .logger.darky_visual import Visual, STYLE, BG, FG
from .utils.config_loader import Configuration
from .handlers.exceptions import AuthError

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

CONFIG = Configuration().get_config()

api_logger = DarkyLogger(logger_name="DARKY_API", configuration=CONFIG.LOGGER)
framework_logger = DarkyLogger(logger_name="DARKY_VK", configuration=CONFIG.LOGGER)
Visual.ansi()
   
class DarkyVK:

    def __init__(self, 
                 ACCESS_TOKEN:str=None, 
                 GROUP_ID:int=None, 
                 API_VERSION:str=CONFIG.vk_api.version) -> None:

        '''
        Initializes DarkyVK as module

        :param ACCESS_TOKEN: your group's access token, you can find it here(https://dev.vk.com/ru/api/access-token/community-token/in-community-settings)
        :type ACCESS_TOKEN: str

        :param GROUP_ID: your group's id, you can find it in your group's settings
        :type GROUP_ID: int

        :param API_VERSION: version of VK API, by default its grabbed from the frameworks's default configuration
        :type API_VERSION: str | None
        '''

        self.__stop_required__ = False
        self.__access_token__ = ACCESS_TOKEN
        self.__group_id__ = GROUP_ID
        self.__api_version__ = API_VERSION

        if ACCESS_TOKEN == None:
            raise AuthError("ACCESS_TOKEN is None!")
        
        if GROUP_ID == None:
            raise AuthError("GROUP_ID is None!")

    async def run(self):
        framework_logger.info(f"{FG.BLUE}DarkyVK is started{STYLE.RESET}")
        while not self.__stop_required__:
            async for event in self.listen():
                ...
        framework_logger.info(f"{FG.RED}DarkyVK has been stopped!{STYLE.RESET}")
    
    async def listen():
        ...

    def stop(self):
        framework_logger.debug(f"DarkyVK was asked to stop")
        self.__stop_required__ = True


class DarkyAPI:

    def __init__(self,
                 HOST:str=CONFIG.api.host,
                 PORT:str=CONFIG.api.port,
                 FRAMEWORK:object=None):
        
        '''
        Initializes DarkyVK as separate API
        
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

        self.__router__ = APIRouter()
        self.__router__.add_api_route("/ping", self.ping, methods=["GET"], 
                                  tags=["API"], name=CONFIG.api.routes.ping.name,
                                  description=CONFIG.api.routes.ping.description)
        self.__router__.add_api_route("/stop", self.stop, methods=["GET"],
                                      tags=["API"], name=CONFIG.api.routes.stop.name,
                                      description=CONFIG.api.routes.stop.description)
        self.__router__.add_api_route("/favicon.ico", self.favicon, include_in_schema=False, methods=["GET"])

        self.__api__.include_router(self.__router__)

    def start(self):
        try:
            api_logger.info(f"Starting...")

            uvicorn_config = uvicorn.Config(
                app=self.__api__,
                host=self.__HOST__,
                port=self.__PORT__,
                log_config=CONFIG.LOGGER
            )
            self.__uvicorn_server__ = uvicorn.Server(uvicorn_config)
            
            api_logger.debug("Starting API Thread...")
            self.__api_thread__ = Thread(
                target=lambda: asyncio.run(self.__uvicorn_server__.serve()),
                daemon=False
            )
            self.__api_thread__.start()

            api_logger.debug("Starting Framework Thread...")
            while self.__framework__ == None:
                pass

            self.__framework_thread__ = Thread(
                target=lambda: asyncio.run(self.__framework__.run()),
                daemon=False
            )
            self.__framework_thread__.start()
        except Exception as e:
            api_logger.error(f"Failed to start API: {e}")
            raise
    
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
            for callback in self.__startup_callbacks__:
                await self.__callback_func__(callback)
            if self.__framework__ == None:
                api_logger.warning(f"Framework was not configured!")
                api_logger.info(f"Initializing default DarkyVK...")
                self.__framework__ = DarkyVK("123", 123)
            api_logger.info(f"{FG.BLUE}Darky API is started{STYLE.RESET} (on {CONFIG.api.host}:{CONFIG.api.port})")
            yield
            '''Here is the shutdown code'''
            for callback in self.__shutdown_callbacks__:
                await self.__callback_func__(callback)
            api_logger.info(f"{FG.RED}Darky API has been stopped{STYLE.RESET}")
        except Exception as e:
            api_logger.error(f"Failed to start API: {e}")
            await self.__shutdown_api__()
            raise

    async def get_api(self):
        return self.__api__
    
    async def ping(self):
        return {"response": "pong"}
    
    async def stop(self):
        
        if not self.__shutdown_initiated__:
            self.__shutdown_initiated__ = True

        api_logger.info("Shutdown initiated!")
        await asyncio.create_task(self.__shutdown_api__())
        return {"response": "shutdown initiated!"}
    
    async def __shutdown_api__(self):

        if self.__uvicorn_server__:
            api_logger.debug(f"Shutting down the API...")
            self.__uvicorn_server__.should_exit = True
            await asyncio.sleep(0.1)
        
        if self.__framework__:
            api_logger.debug(f"Shutting down the framework...")
            self.__framework__.stop()
    
    async def favicon(self):
        return FileResponse(ASSETS / "favicon.ico")