import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from logger.darky_logger import DarkyLogger
from utils.darky_visual import Visual, STYLE, BG

from utils.tools import Configuration

logger = DarkyLogger(logger_name="DARKYVK", configuration=Configuration().config["LOGGER"])
Visual.ansi()

class DarkyVK:

    def __init__(self):
        ...

def main():
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8000)

@asynccontextmanager
async def lifespan(api: FastAPI):
    '''
    Provides start_up(preparing API wrapper) and
    shut_down(saving data for example) event handling
    '''
    '''Here is the startup'''
    logger.info(f"DarkyVK API is starting up...")
    yield
    '''Here is the shutdown'''
    logger.info(f"DarkyVK API is shutting down...")

api = FastAPI(lifespan=lifespan)

@api.get("/ping")
async def ping():
    return {"response": "pong"}

if __name__ == "__main__":
    main()