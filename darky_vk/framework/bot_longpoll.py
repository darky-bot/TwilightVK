import asyncio

from ..utils.config_loader import Configuration
from ..http.async_http import Http
from ..logger.darky_logger import DarkyLogger
from ..logger.darky_visual import FG, STYLE

CONFIG = Configuration().get_config()

httpClient = Http()

logger = DarkyLogger("botlongpoll", configuration=CONFIG.LOGGER)

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
    
    async def auth(self):

        '''
        Authorizing framework in VK API by getting LongPoll server
        '''

        try:
            logger.debug(f"Authorization...")
            logger.debug(f"Getting Bots LongPoll Server...")
            response = await httpClient.get(url=f"{self.__api_url__}/method/groups.getLongPollServer",
                                        params={
                                            "access_token":self.__access_token__,
                                            "v": self.__api_version__,
                                            "group_id": self.__group_id__
                                        },
                                        raw=False)
            
            if "error" in response:
                ...

            response = response["response"]
            logger.debug(f"Server aquired: {response}")
            self.__key__ = response["key"]
            self.__server__ = response["server"]
            self.__ts__ = response["ts"]
            self.authorized = True
            logger.debug(f"Authorized")
        except KeyError as ex:
            logger.error(f"Unable to find key: {ex} {response}")
    
    async def check_event(self) -> dict:
        
        '''
        Getting the event from BotsLongPoll server
        '''
        try:
            self.wait_for_response=True
            logger.debug(f"Listening the BotsLongPoll server for events...")
            response = await httpClient.get(url=f"{self.__server__}",
                                            params={
                                                "act": "a_check",
                                                "key": self.__key__,
                                                "ts": self.__ts__,
                                                "wait": self.__wait__
                                            },
                                            raw=False)
            logger.debug(f"Got an event: {response}")
            self.wait_for_response=False
            return response
        except KeyError as ex:
            logger.error(f"Unable to find key: {ex} {response}")
    
    async def listen(self):

        '''
        Listening for events
        '''
        try:
            logger.debug(f"Polling was started")
            while not self.__stop__:
                event = await self.check_event()

                if "failed" in event:
                    ...
                
                if "ts" not in event:
                    self.auth()
                
                self.__ts__ = event["ts"]
                
                if "updates" not in event or event["updates"] == []:
                    continue

                yield event
            
        except asyncio.CancelledError:
            logger.warning(f"Polling was forcibly canceled (it is not recommend to do this)")
        finally:
            await httpClient.close()
            logger.debug(f"Polling was stopped")
        
    def stop(self):
        logger.debug(f"Polling will be stopped as soon as the current event is recieved")
        self.__stop__ = True
    
    async def cancelPolling(self):
        await httpClient.close()
        logger.warning(f"Polling was cancelled. HttpClient was closed")