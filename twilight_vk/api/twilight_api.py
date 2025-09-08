import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from ..components.logo import LogoComponent
from ..logger.darky_logger import DarkyLogger
from ..logger.darky_visual import STYLE, FG, BG, Visual
from ..utils.config_loader import Configuration
from .routers.root import RootRouter

if TYPE_CHECKING:
    from ..framework.twilight_vk import TwilightVK

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

CONFIG = Configuration().get_config()

Visual.ansi()

class TwilightAPI:

    def __init__(self,
                 BOTS: object | list[object],
                 HOST: str = CONFIG.api.host,
                 PORT: str = CONFIG.api.port,
                ):
        '''
        API Swagger for bots based on Twilight framework

        :param BOTS: One or list of initialized Twilight bot objects
        :type BOTS: object | list[object]

        :param HOST: Sets the host ip adress for API Swagger
        :type HOST: str

        :param PORT: Sets the port for API Swagger
        :type PORT: str
        '''
        self.logo = LogoComponent()
        self.logger = DarkyLogger(logger_name=f"twilight-api", configuration=CONFIG.LOGGER)
        
        self.logger.debug(f"Initializing API...")

        self.__shutdown_initiated__ = False

        self.__HOST__ = HOST
        self.__PORT__ = PORT

        self.__api__ = FastAPI(
            title=CONFIG.api.title,
            description=CONFIG.api.description,
            version=CONFIG.api.version,
            lifespan=self.lifespan
        )

        self.bots:list['TwilightVK'] = BOTS

        self.__loop__ = asyncio.get_event_loop()

        uvicorn_config = uvicorn.Config(
                app=self.__api__,
                host=self.__HOST__,
                port=self.__PORT__,
                log_config=CONFIG.LOGGER,
            )
        self.__uvicorn_server__ = uvicorn.Server(uvicorn_config)

        self.__api__.include_router(RootRouter(self.stop).get_router())

        self.router = APIRouter(
            tags=["Server"]
        )
        self.router.add_api_route(path="/favicon.ico", endpoint=self.favicon, methods=["GET"],
                                  include_in_schema=False)
        self.__api__.include_router(self.router)

        self.logger.initdebug(f"Importing bot's API routers...")
        for bot in self.bots:
            self.logger.initdebug(f"Importing API routers from {bot.__class__.__name__} - bot[{self.bots.index(bot)}]...")
            self.__api__.include_router(bot.__getApiRouters__())
        else:
            self.logger.initdebug(f"There is no connected bots to the API")
        
        self.logger.debug(f"API is initialized")

    @asynccontextmanager
    async def lifespan(self, api: FastAPI):
        '''
        Provides start_up(preparing API wrapper) and
        shut_down(saving data for example) event handling
        '''
        try:
            '''Here is the startup code'''
            self.logger.info(f"Twilight API is starting...")
            ...
            self.logger.info(f"{FG.BLUE}Twilight API is started (on {CONFIG.api.host}:{CONFIG.api.port}){STYLE.RESET}")

            yield

            '''Here is the shutdown code'''
            self.logger.info(f"{FG.RED}Twilight API is stopped{STYLE.RESET}")
        except Exception as ex:
            self.logger.critical(f"Unhandled error", exc_info=True)
            await self.stop()
    
    async def favicon(self) -> FileResponse:
        '''
        THIS IS API METHOD
        '''
        return FileResponse(ASSETS / "favicon.ico")

    def start(self):
        '''
        Starts the API Swagger
        '''
        try:
            self.logger.note(self.logo.colored)
            self.__loop__.run_until_complete(self.__uvicorn_server__.serve())
        except KeyboardInterrupt:
            self.logger.warning(f"KeyboardInterrupt was recieved")
        except Exception as ex:
            self.logger.critical(f"Unhandled error", exc_info=True)
        finally:
            self.__loop__.run_until_complete(self.__loop__.shutdown_asyncgens())
            self.__loop__.close()

    async def stop(self):
        '''
        Shutdown the API Swagger
        '''
        if self.__uvicorn_server__.started:
            self.logger.info(f"Shutting down the API...")
            self.__uvicorn_server__.should_exit = True
            await asyncio.sleep(0.1)
    
    #TODO: importing routers from bots