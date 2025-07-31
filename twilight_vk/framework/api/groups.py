from .api import BaseMethodsGroup

class Groups(BaseMethodsGroup):
    
    async def getLongPollServer(self,
                                group_id:int) -> dict:
        
        '''
        Returns data for connection to Bots Longpoll API

        :param group_id: - Group's ID
        :type group_id: int
        '''

        values = {
            "group_id": abs(group_id),
            "v": self.__api_version__
        }
        response = await self.base_api.base_get_method(api_method=f"{self.method}.getLongPollServer",
                                                       values=values)
        return response
    