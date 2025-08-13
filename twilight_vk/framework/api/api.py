from aiohttp import ClientResponse

from ...http.async_http import Http
from ...logger.darky_logger import DarkyLogger
from ...utils.config_loader import Configuration
from ..validators.http_validator import HttpValidator
from ..validators.event_validator import EventValidator

CONFIG = Configuration().get_config()

class VkBaseMethods:

    def __init__(self,
                 url:str,
                 token:str,
                 group:int):
        self.__url__ = url
        self.__token__ = token
        self.__group__ = group
        self.httpValidator = HttpValidator()
        self.eventValidator = EventValidator()
        self.httpClient = Http({"Authorization": f"Bearer {token}"})
        self.logger = DarkyLogger("vk-methods", configuration=CONFIG.LOGGER)

    async def base_get_method(
            self,
            api_method:str,
            values:dict={},
            headers:dict={},
            validate:bool=True
            ) -> ClientResponse:
        valid_values = {}
        for key, value in values.items():
            if value not in ['', None]:
                valid_values[key] = value
        self.logger.debug(f"Calling HTTP-GET {api_method} method with {values} {headers}...")
        response = await self.httpClient.get(url=f"{self.__url__}/method/{api_method}",
                                            params=valid_values,
                                            headers=headers,
                                            raw=True)
        if validate:
            response = await self.httpValidator.validate(response)
            response = await self.eventValidator.validate(response)

        self.logger.debug(f"Response for {api_method}: {response}")
        return response
        
    async def base_post_method(
            self,
            api_method:str,
            values:dict={},
            data:dict={},
            headers:dict={},
            validate:bool=True
            ) -> ClientResponse:
        valid_values = {}
        for key, value in values.items():
            if value not in ['', None]:
                valid_values[key] = value
        self.logger.debug(f"Calling HTTP-POST {api_method} method with {values} {headers}:{data}...")
        response = await self.httpClient.post(url=f"{self.__url__}/method/{api_method}",
                                            params=valid_values,
                                            data=data,
                                            headers=headers,
                                            raw=True)
        if validate:
            response = await self.httpValidator.validate(response)
            response = await self.eventValidator.validate(response)

        self.logger.debug(f"Response for {api_method}: {response}")
        return response
    
    async def close(self):
        self.logger.debug("VkBaseMethods was closed")
        await self.httpClient.close()


class BaseMethodsGroup:

    def __init__(self,
                 baseMethods:VkBaseMethods):
        self.__access_token__ = baseMethods.__token__
        self.__group_id__ = baseMethods.__group__
        self.__api_version__ = CONFIG.vk_api.version
        self.base_api = baseMethods
        self.__class_name__ = self.__class__.__name__
        self.method = f"{self.__class_name__[0].lower()}{self.__class_name__[1:]}"