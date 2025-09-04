import asyncio
import aiohttp
import aiohttp.client_exceptions

from ..utils.config_loader import Configuration
from ..logger.darky_logger import DarkyLogger
from ..logger.darky_visual import FG, STYLE
from ..http.async_http import Http
from .api.api import VkBaseMethods
from .api.methods import VkMethods
from .validators.http_validator import HttpValidator
from .validators.event_validator import EventValidator
from .handlers.exceptions import AuthError, VkApiError
from .handlers.events import EventHandler

CONFIG = Configuration().get_config()

class BotsLongPoll:

    def __init__(self, access_token:str=None, group_id:int=None, api_version:str|None=CONFIG.vk_api.version):
        '''
        BotLongPoll provides a communication between your app and VK API
        Bots Long Poll API allows you to process community events in real time

        :param access_token: your group's access token, you can find it here(https://dev.vk.com/ru/api/access-token/community-token/in-community-settings)
        :type access_token: str

        :param group_id: your group's id, you can find it in your group's settings
        :type group_id: int

        :param api_version: version of VK API, by default its grabbed from DarkyVK's configuration
        :type api_version: str | None
        '''

        self.__stop__ = False
        self.__is_polling__ = False
        self.__access_token__ = access_token
        self.__group_id__ = group_id
        self.__api_url__ = CONFIG.vk_api.server
        self.__api_version__ = api_version
        self.__server__ = None
        self.__key__ = None
        self.__ts__ = None
        self.__wait__ = CONFIG.vk_api.wait
        self.authorized = False
        self.wait_for_response = False
        self.httpValidator = HttpValidator()
        self.eventValidator = EventValidator()
        self.httpClient = Http()
        self.base_methods = VkBaseMethods(self.__api_url__, self.__access_token__, self.__group_id__)
        self.vk_methods = VkMethods(self.base_methods)
        self.event_handler = EventHandler(self.vk_methods)
        self.on_event = self.event_handler.on_event
        self.logger = DarkyLogger("botlongpoll", configuration=CONFIG.LOGGER)
    
    def get_vk_methods(self):
        return self.vk_methods
    
    def get_event_handler(self):
        return self.event_handler
    
    async def auth(self):

        '''
        Authorizing framework in VK API by getting LongPoll server
        '''

        try:
            self.logger.debug(f"Authorization...")

            self.logger.debug(f"Getting Bots LongPoll Server...")
            self.wait_for_response = True
            response = await self.vk_methods.groups.getLongPollServer()
            response = response["response"]
            self.wait_for_response = False
            self.logger.debug(f"Server aquired: {response}")

            self.__key__ = response["key"]
            self.__server__ = response["server"]
            self.__ts__ = response["ts"]
            self.authorized = True

            self.logger.debug(f"Authorized")

        except aiohttp.client_exceptions.ClientConnectorDNSError as ex:
            self.logger.critical(f"{ex}", exc_info=True)
            self.stop()
        except AuthError as ex:
            self.logger.error(f"Authrization error: {ex}")
            self.stop()
        except VkApiError as ex:
            self.logger.critical("Request to VK API was handled with error", exc_info=True)
            self.stop()

    
    async def check_event(self) -> dict:
        
        '''
        Getting the event from BotsLongPoll server
        '''
        try:
            self.wait_for_response=True
            self.logger.debug(f"Listening the BotsLongPoll server for events...")
            response = await self.httpClient.get(url=f"{self.__server__}",
                                            params={
                                                "act": "a_check",
                                                "key": self.__key__,
                                                "ts": self.__ts__,
                                                "wait": self.__wait__
                                            },
                                            raw=True)
            self.logger.debug(f"Validating...")
            response = await self.httpValidator.validate(response)
            response = await self.eventValidator.validate(response, from_polling=True)
            self.logger.debug(f"Got an event: {response}")
            self.wait_for_response=False

            if "ts" not in response:
                self.auth()

            self.__ts__ = response["ts"]
            
            return response
        except VkApiError as ex:
            self.logger.critical("Request to VK API was handled with error", exc_info=True)
            self.stop()
    
    async def listen(self):

        '''
        Listening for events
        '''
        try:
            self.logger.debug(f"Polling was started")
            self.__is_polling__ = True
            while not self.__stop__:
                event = await self.check_event()
                
                if "updates" not in event or event["updates"] == []:
                    continue

                yield event
        
        except asyncio.CancelledError:
            self.logger.warning(f"Listening was forcibly canceled (it is not recommend to do this)")
        finally:
            await self.httpClient.close()
            await self.base_methods.close()
            self.__is_polling__ = False
            self.logger.debug(f"Polling was stopped")
        
    def stop(self):
        if self.__stop__ != True and (self.__is_polling__ or self.wait_for_response):
            self.logger.info(f"Polling will be stopped as soon as the current request will be done. Please wait")
            self.__stop__ = True