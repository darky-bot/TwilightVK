import requests

#from darky_vk import api_config
from logger.darky_logger import DarkyLogger
#from darky_vk.framework.methods import messages
#from darky_vk.framework.handlers.errors import ApiError

logger = DarkyLogger()

class BotsLongPollEvents():

    MESSAGE_NEW = 'message_new'

    MESSAGE_TYPING_STATE = "message_typing_state"


class BotsLongPoll():

    def __init__(self, access_token:str=None, group_id:int=None, api_version:str=api_config.__api_version__, error_handlers:dict=None, wait:int=25) -> None:
        self.__access_token__ = access_token
        self.__group_id__ = group_id
        self.__api_version__ = api_version
        self.__key__ = None
        self.__server__ = None
        self.__ts__ = None
        self.__error_handlers__ = error_handlers
        self.__stop__ = False
        self.__wait__ = wait
    
    @staticmethod
    def get_response(response) -> dict:

        if "error" in response:
            raise ApiError(response["error"])
        
        if "response" in response:
            return response["response"]
    
    def auth(self):

        logger.debug("Authorization...")

        logger.debug(f"Getting Bots LongPoll API Server...")
        response = self.get_response(requests.get(url=f"https://api.vk.com/method/groups.getLongPollServer",
                     params={
                         "access_token":self.__access_token__,
                         "v": self.__api_version__,
                         "group_id": self.__group_id__
                     }).json())
        
        self.__key__ = response["key"]
        self.__server__ = response["server"]
        self.__ts__ = response["ts"]
        logger.debug(f"Server acquired: {response}")

        logger.debug(f"Authorized")
    

    async def check_event(self) -> dict:

        logger.debug(f"Listening the LongPoll API Server for events...")
        response = self.get_response(requests.get(url=f"{self.__server__}",
                      params={
                          "act": "a_check",
                          "key": self.__key__,
                          "ts": self.__ts__,
                          "wait": self.__wait__
                      }).json())
        logger.debug(f"Got an event: {response}")
        return response


    async def listen(self):

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

        logger.info(f"Listening was stopped")
    

    async def stop(self):
        self.__stop__ = True