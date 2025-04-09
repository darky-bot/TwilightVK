import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from logger.darky_logger import DarkyLogger
from utils.darky_visual import Visual, STYLE, BG

logger = DarkyLogger()
Visual.ansi()

class DarkyVK:

    def __init__(self, access_token:str=None, group_id:int=None, api_version:str=None):
        
        logger.info('Preparing DarkyVK...')
        self.api = FastAPI()
        self.api.router.lifespan_context = self.lifespan
        
        self.api.add_api_route("/hello", self.run, methods=["GET"])
        #self.api = FastAPI(lifespan=self.lifespan)
        #self.bot = ...
        #self.bot.auth()
        logger.info(f'{BG.BLUE}DarkyVK is ready{STYLE.RESET}')
    
    @asynccontextmanager
    async def lifespan(self, api: FastAPI):
        '''
        Provides start_up(preparing API wrapper) and 
        shut_down(saving data, for example) event handling
        '''
        '''Here is the startup'''
        logger.info(f"Starting DarkyVK API...")
        yield
        '''Here is the shutdown'''
        logger.info(f"Shutting down DarkyVK API...")
    
    async def run(self):
        return {"Hello": "World"}
    
    def reauth(self):
        ...
    
    async def run_polling(self):
        ...
    
    async def stop(self):
        ...
    
bot = DarkyVK().api