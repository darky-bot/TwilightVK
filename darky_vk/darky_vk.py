import asyncio
from pathlib import Path

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from .logger.darky_logger import DarkyLogger
from .utils.darky_visual import Visual, STYLE, BG
from .utils.config_loader import Configuration
from .handlers.exceptions import AuthError

CONFIG = Configuration().get_config()

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

logger = DarkyLogger(logger_name="DARKYVK", configuration=CONFIG.LOGGER)
Visual.ansi()

class DarkyVK:

    '''Initializes DarkyVK as module'''

    def __init__(self, access_token:str=None, group_id:int=None, api_version:str=CONFIG.vk_api.version) -> None:
        self.__access_token__ = access_token
        self.__group_id__ = group_id
        self.__api_version__ = api_version

        if access_token == None:
            raise AuthError("ACCESS_TOKEN is None!")
        
        if group_id == None:
            raise AuthError("GROUP_ID is None!")

    def run(self):
        ...


class DarkyAPI(DarkyVK):

    '''Initializes DarkyVK as separate API'''

    def __init__(self):
        self.api = FastAPI(
            title=CONFIG.api.title,
            description=CONFIG.api.description,
            version=CONFIG.api.version,
            lifespan=self.lifespan
            )

        self.router = APIRouter()
        self.router.add_api_route("/ping", self.ping, methods=["GET"], 
                                  tags=["Server"], name="Pings the server",
                                  description="Pings the server, not the submodules and subdomains such as /darky_db etc.")
        self.router.add_api_route("/favicon.ico", self.favicon, include_in_schema=False, methods=["GET"])

        self.api.include_router(self.router)

    def start(self):
        try:
            uvicorn.run(self.api, host=CONFIG.api.host, port=CONFIG.api.port)
        except Exception as e:
            logger.error(f"Failed to start API: {e}")
            raise

    def close(self):
        raise KeyboardInterrupt
    
    @asynccontextmanager
    async def lifespan(self, api: FastAPI):
        '''
        Provides start_up(preparing API wrapper) and
        shut_down(saving data for example) event handling
        '''
        '''Here is the startup code'''
        logger.info(f"DarkyVK API is starting up...")
        yield
        '''Here is the shutdown code'''
        logger.info(f"DarkyVK API is shutting down...")

    def get_api(self):
        return self.api
    
    async def ping(self):
        return {"response": "pong"}
    
    async def favicon(self):
        return FileResponse(ASSETS / "favicon.ico")

if __name__ == "__main__":
    api = DarkyAPI().get_api()
    DarkyAPI().start()