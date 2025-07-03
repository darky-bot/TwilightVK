from aiohttp import ClientResponse

from ...http.async_http import Http
from ...logger.darky_logger import DarkyLogger
from ...utils.config_loader import Configuration
from ..validators.response_validator import ResponseValidator

CONFIG = Configuration().get_config()

class VkMethods:

    def __init__(self,
                 url:str,
                 token:str,
                 validate_response:bool=True):
        self.__url__ = url
        self.__token__ = token
        self.validate = validate_response
        self.httpClient = Http()
        self.logger = DarkyLogger("vk-methods", configuration=CONFIG.LOGGER)

    async def base_get_method(
            self,
            api_method:str,
            values:dict={},
            raw:bool=False
            ) -> ClientResponse:
        try:
            self.logger.debug(f"Calling HTTP-GET {api_method} method with {values}...")
            response = await self.httpClient.get(url=f"{self.__url__}/method/{api_method}",
                                                params=values,
                                                raw=raw)
            if type(response) == dict:
                ...
            self.logger.debug(f"Response for {api_method}: {response}")
            return response
        except Exception as ex:
            self.logger.error(f"Error with calling {api_method}", exc_info=True)
    
    async def close(self):
        self.logger.debug("VkMethods was closed")
        await self.httpClient.close()