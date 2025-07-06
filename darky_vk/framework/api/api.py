from aiohttp import ClientResponse

from ...http.async_http import Http
from ...logger.darky_logger import DarkyLogger
from ...utils.config_loader import Configuration
from ..validators.response_validator import ResponseValidator

CONFIG = Configuration().get_config()

class VkBaseMethods:

    def __init__(self,
                 url:str,
                 token:str,
                 validate_response:bool=True):
        self.__url__ = url
        self.__token__ = token
        self.validate = validate_response
        self.validator = ResponseValidator()
        self.httpClient = Http()
        self.logger = DarkyLogger("vk-methods", configuration=CONFIG.LOGGER)

    async def base_get_method(
            self,
            api_method:str,
            values:dict={}
            ) -> ClientResponse:
        try:
            self.logger.debug(f"Calling HTTP-GET {api_method} method with {values}...")
            response = await self.httpClient.get(url=f"{self.__url__}/method/{api_method}",
                                                params=values,
                                                raw=True)
            self.logger.debug(f"Validating response for {api_method}...")
            response = await self.validator.validate(response)

            self.logger.debug(f"Response for {api_method}: {response}")
            return response
        except Exception as ex:
            self.logger.critical(f"Error with calling {api_method}", exc_info=True)
            await self.close()
        
    async def base_post_method(
            self,
            api_method:str,
            values:dict={},
            data:dict={},
            headers:dict=None
            ) -> ClientResponse:
        try:
            self.logger.debug(f"Calling HTTP-POST {api_method} method with {values} {headers}:{data}...")
            response = await self.httpClient.post(url=f"{self.__url__}/method/{api_method}",
                                                params=values,
                                                data=data,
                                                headers=headers,
                                                raw=True)
            self.logger.debug(f"Validating response  for {api_method}...")
            response = await self.validator.validate(response)

            self.logger.debug(f"Response for {api_method}: {response}")
            return response
        except Exception as ex:
            self.logger.critical(f"Error with calling {api_method}", exc_info=True)
            await self.close()
    
    async def close(self):
        self.logger.debug("VkBaseMethods was closed")
        await self.httpClient.close()


class BaseMethodsGroup:

    def __init__(self,
                 baseMethods:VkBaseMethods):
        self.__access_token__ = baseMethods.__token__
        self.__api_version__ = CONFIG.vk_api.version
        self.base_api = baseMethods
        self.__class_name__ = self.__class__.__name__
        self.method = f"{self.__class_name__[0].lower()}{self.__class_name__[1:]}"