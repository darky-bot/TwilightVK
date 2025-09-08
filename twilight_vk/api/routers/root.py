from typing import Callable
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from .base import BaseRouter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS = BASE_DIR / "assets"

class RootRouter(BaseRouter):

    def __init__(self,
                 stop_command: Callable = None):

        self.router = APIRouter(
            tags=["Root"],
            prefix="/api/v1/root"
        )

        self.stop_command = stop_command
        
        self.router.add_api_route("/ping", self.ping, methods=["GET"], 
                                  name="Pings the API",
                                  description="Method for API status check. Should return \"pong\" if alive.")
        self.router.add_api_route("/stop", self.stop, methods=["GET"],
                                  name="Stops the API",
                                  description="Stops all routers of API and API itself")
    
    async def ping(self) -> dict:
        return {"response": "Pong OwO!"}
    
    async def stop(self) -> dict:
        await self.stop_command()
        return {"response": "Shutdown initiated!"}