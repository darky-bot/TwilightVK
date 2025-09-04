from random import randint

from .api import BaseMethodsGroup

class Messages(BaseMethodsGroup):
    
    async def send(self,
                   user_id: int | str = None,
                   peer_id: int | str = None,
                   peer_ids: str | list[str] | int | list[int] = None,
                   domain:str=None,
                   chat_id:int=None,
                   user_ids:str|list[int]=None,
                   message:str=None,
                   lat:str=None,
                   long:str=None,
                   attachment:str|list[str]=None,
                   reply_to:int=None,
                   forward_messages:str|list[int]=None,
                   forward:dict=None,
                   sticker_id:int=None,
                   group_id:int=None,
                   keyboard:object=None,
                   template:object=None,
                   payload:object=None,
                   content_source:dict=None,
                   dont_parse_links:bool=None,
                   disable_mentions:bool=None,
                   intent:str=None,
                   subsribe_id:int=None,
                   **kwargs):
        
        '''
        Отправляет сообщение

        :param user_id: Обязательный параметр. Идентификатор пользователя, которому отправляется сообщение. Вместо него можно использовать peer_id.
        :type user_id: int | str

        :param peer_id: Необязательный параметр. Идентификатор получателя сообщения:\n
            - Для пользователя — ИДЕНТИФИКАТОР_ПОЛЬЗОВАТЕЛЯ.\n
            - Для групповой беседы — 2000000000 + ИДЕНТИФИКАТОР_БЕСЕДЫ.\n
            - Для сообщества — -ИДЕНТИФИКАТОР_СООБЩЕСТВА.\n
        :type peer_id: int | str

        :param peer_ids: Идентификаторы получателей сообщения, перечисленные через запятую. Максимальное количество идентификаторов — 100.
        :type peer_ids: str | list
        '''

        values = {
            "user_id": user_id,
            "random_id": randint(0, 1000000000),
            "peer_id": peer_id,
            "peer_ids": peer_ids,
            "message": message,
            "group_id": abs(group_id) if group_id is not None else self.__group_id__,
            "reply_to": reply_to,
            "forward": forward,
            "v": self.__api_version__
        }
        response = await self.base_api.base_get_method(api_method=f"{self.method}.send",
                                                       values=values,
                                                       validate=False)
        return response