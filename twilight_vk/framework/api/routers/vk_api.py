from typing import TYPE_CHECKING
import logging
import re
import inspect

from fastapi import APIRouter

if TYPE_CHECKING:
    from ...twilight_vk import TwilightVK

class VkApiRouter:

    def __init__(self, _bot: 'TwilightVK') -> None:
        '''
        Framework's VkApi methods API router

        :param bot: TwilightVK object
        :type bot: TwilightVK
        '''
        self.logger = logging.getLogger("twi-api-vkapi")
        self.logger.log(1, f"VkApi API Router was initialized")
        self.bot = _bot

        self.router = APIRouter(
            tags=[f"{self.bot.bot_name}.methods"],
            prefix=f"/vk-methods"
        )
    
    def get_router(self) -> APIRouter:
        return self.router