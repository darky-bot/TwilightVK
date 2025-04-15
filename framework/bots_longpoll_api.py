from utils.tools import Configuration

config = Configuration().config["api"]

class BotsLongPoll:

    def __init__(self, access_token:str=None, group_id:int=None, api_version:str|None=config["version"]):
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

        self.__access_token__ = access_token
        self.__group_id__ = group_id
        self.__api_url__ = config["server"]
        self.__api_version__ = api_version
        self.__server__ = None
        self.__key__ = None
        self.__ts__ = None
        self.__wait__ = config["wait"]
    
    def auth(self):
        ...