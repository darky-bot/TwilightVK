from aiohttp import ClientResponse
from http import HTTPStatus

from ...utils.config_loader import Configuration
from ...logger.darky_logger import DarkyLogger
from ..exceptions.validator import HttpValidationError

CONFIG = Configuration().get_config()

class HttpValidator:

    def __init__(self):
        self.logger = DarkyLogger("http-validator", CONFIG.LOGGER, silent=True)

    async def __isValid__(self,
                          response:ClientResponse) -> bool:
        self.logger.debug(f"Type matching check...")
        if type(response) != ClientResponse:
            self.logger.error(f"Types does not match: {type(response)} != {ClientResponse}")
            return False
        return True
    
    async def __isSuccess__(self,
                            response:ClientResponse) -> bool:
        self.logger.debug(f"HTTP Status check...")
        if response.status != HTTPStatus.OK:
            self.logger.error(f"HTTP status is {response.status}")
            return False
        return True


    async def validate(self,
                       response:ClientResponse) -> ClientResponse:
        self.logger.debug(f"Validating response for [{response.method}] \"{response.url}\"...")

        isValid = await self.__isValid__(response)
        isSuccess = await self.__isSuccess__(response)

        if isValid and isSuccess:
            self.logger.debug(f"HTTP Response is valid")
            return response
        
        self.logger.warning(f"HTTP Response is not valid")
        self.logger.warning(f'{"isValid":<10}|{"":>1}{"isSuccess":<10}|{"":>1}{"response":<10}')
        self.logger.warning(f'{isValid:<10}|{"":>1}{isSuccess:<10}|{"":>1}{response}')
        
        raise HttpValidationError(isValid, isSuccess, response)