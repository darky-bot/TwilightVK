import logging

from aiohttp import ClientResponse

from ...http.async_http import Http
from ...utils.config import CONFIG
from ..validators import (
    HttpValidator,
    EventValidator,
    RequestValidator
)

class VkBaseMethods:

    def __init__(self,
                 url:str,
                 token:str,
                 group:int):
        self.__url__ = url
        self.__token__ = token
        self.__group__ = group
        self.httpClientHeaders = {"Authorization": f"Bearer {token}"}
        self.httpClient = Http(self.httpClientHeaders)
        self.logger = logging.getLogger("vk-methods")

    async def base_get_method(
            self,
            api_method:str,
            values:dict={},
            headers:dict={},
            validate:bool=True
            ) -> ClientResponse:
        
        valid_values = await RequestValidator.validate(values)

        headers = headers | self.httpClientHeaders

        self.logger.debug(f"Calling HTTP-GET {api_method} method with {valid_values} {headers if headers != {} else ""}...")
        response = await self.httpClient.get(url=f"{self.__url__}/method/{api_method}",
                                            params=valid_values,
                                            headers=headers,
                                            raw=True)
        if validate:
            response = await HttpValidator.validate(response)
            response = await EventValidator.validate(response)

        self.logger.debug(f"Response for {api_method}: {response if isinstance(response, dict) else f"{response.request_info} <{response.status}>"}")
        return response
        
    async def base_post_method(
            self,
            api_method:str,
            values:dict={},
            data:dict={},
            headers:dict={},
            validate:bool=True
            ) -> ClientResponse:
        
        valid_values = valid_values = await RequestValidator.validate(values)

        headers = headers | self.httpClientHeaders

        self.logger.debug(f"Calling HTTP-POST {api_method} method with {valid_values} {headers if headers != {} else ""}:{data}...")
        response = await self.httpClient.post(url=f"{self.__url__}/method/{api_method}",
                                            params=valid_values,
                                            data=data,
                                            headers=headers,
                                            raw=True)
        if validate:
            response = await HttpValidator.validate(response)
            response = await EventValidator.validate(response)

        self.logger.debug(f"Response for {api_method}: {response if isinstance(response, dict) else f"{response.request_info} <{response.status}>"}")
        return response
    
    async def close(self):
        self.logger.debug("VkBaseMethods was closed")
        await self.httpClient.close()


class BaseMethodsGroup:

    def __init__(self,
                 baseMethods:VkBaseMethods):
        self.__access_token__ = baseMethods.__token__
        self.__group_id__ = baseMethods.__group__
        self.__api_version__ = CONFIG.VK_API.version
        self.base_api = baseMethods
        self.__class_name__ = self.__class__.__name__
        self.logger = logging.getLogger("vk-methods")
        self.logger.log(1, f"Class {self.__class_name__} was initiated")
        self.method = f"{self.__class_name__[0].lower()}{self.__class_name__[1:]}"