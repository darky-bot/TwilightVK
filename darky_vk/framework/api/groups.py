from .api import BaseMethodsGroup
from ...utils.config_loader import Configuration

CONFIG = Configuration().get_config()

class Groups(BaseMethodsGroup):
    
    async def getLongPollServer(self,
                                group_id:int) -> dict:
        
        '''
        Возвращает данные для подключения к Bots Longpoll API
        
        :param group_id: - Идентификатор сообщества.
        :type group_id: int
        '''

        values = {
            "access_token": self.__access_token__,
            "group_id": group_id,
            "v": self.__api_version__
        }
        response = await self.base_api.base_get_method(api_method=f"{self.method}.getLongPollServer",
                                                       values=values)
        return response