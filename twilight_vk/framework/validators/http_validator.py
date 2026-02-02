import logging

from aiohttp import ClientResponse
from http import HTTPStatus

from ..exceptions.validator import HttpValidationError
from ...utils.validation_reports import make_it_colored as color

logger = logging.getLogger("http-validator")

class HttpValidator:

    async def _isValid(response: ClientResponse) -> bool:
        '''
        Response type checking
        '''
        logger.debug(f"HTTP Validation: Type matching check...")

        if type(response) != ClientResponse:
            logger.error(f"Types does not match: {type(response)} != {ClientResponse}")
            return False
        
        return True
    
    async def _isSuccess(response: ClientResponse) -> bool:
        '''
        Http status code check
        '''
        logger.debug(f"HTTP Validation: HTTP Status check...")

        if response.status >= HTTPStatus.BAD_REQUEST:
            logger.error(f"HTTP status code is {response.status}")
            return False
        
        return True


    async def validate(response: ClientResponse) -> ClientResponse:
        '''
        Validating http response
        '''
        logger.debug(f"Validating http response for [{response.method}] \"{response.url}\"...")

        isValid = await HttpValidator._isValid(response)
        isSuccess = None

        if isValid:
            isSuccess = await HttpValidator._isSuccess(response)

        if isValid and isSuccess:
            logger.debug(f"HTTP Response is valid")
            return response
        
        logger.warning(f"HTTP Response is not valid")
        logger.warning(f'{"Raw is valid":<15}|{"":>1}{"Is success":<15}|{"":>1}{"response":<10}')
        logger.warning(f'{color(isValid, indent=15)}|{"":>1}{color(isSuccess, indent=15)}|{"":>1}{color(response)}')
        
        raise HttpValidationError(isValid, isSuccess, response)