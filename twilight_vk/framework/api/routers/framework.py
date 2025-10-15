import re
from typing import TYPE_CHECKING

from fastapi import APIRouter

from ....logger.darky_logger import DarkyLogger
from ....utils.config import CONFIG

if TYPE_CHECKING:
    from ...twilight_vk import TwilightVK

class FrameworkRouter:

    def __init__(self, bot: 'TwilightVK'):

        self.logger = DarkyLogger(logger_name="twi-api-fw", configuration=CONFIG.LOGGER)
        self.logger.initdebug(f"Framework API Router was initiated")
        self.bot = bot

        self.router = APIRouter(
            tags=[bot.bot_name],
            prefix=f"/{re.escape(bot.bot_name)}"
        )

        self.router.add_api_route("/ping", self.ping, methods=["GET"],
                                  name="Ping Framework API",
                                  description="Pings the frameworks's main API router")
        self.router.add_api_route("/stop", self.stop, methods=["GET"],
                                  name="Stop Current Bot",
                                  description="Stops current linked bot")
    
    async def ping(self):
        return {"response": {"message": "Pong OwO"}}
    
    async def stop(self, force=False):
        self.bot.stop(force, self.bot.__tasks__)
        return {"response": {"message": "Bot was stopped", "forced": force}}

    
    def get_router(self):
        return self.router