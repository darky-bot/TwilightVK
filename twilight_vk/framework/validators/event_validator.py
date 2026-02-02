import logging

from aiohttp import ClientResponse

from ...utils.config import CONFIG
from ..exceptions.validator import (
    EventValidationError
)
from ..exceptions.vkapi import (
    VkApiError,
    AuthError,
    LongPollError
)
from ...utils.validation_reports import make_it_colored as color

logger = logging.getLogger('event-validator')

class EventValidator:

    _requiredFields = ['response', 'error']
    _pollingRequiredFields = ['updates', 'failed']
    _errorFields = [
        _requiredFields[-1],
        _pollingRequiredFields[-1]
    ]

    async def _isJsonValid(response: ClientResponse) -> bool:
        '''
        Check the JSON in the response
        '''
        logger.debug(f"Event Validaion: Checking Content-Type header for JSON...")

        _content_type = response.headers.get('Content-Type', None)

        if not _content_type or _content_type != 'application/json':
            logger.error(f"Response doesn't have JSON content")
            return False
        
        return True
    
    async def _fieldsAreValid(content: dict,
                              fields: dict={}) -> bool:
        '''
        Check required fields in the response
        '''
        logger.debug(f"Event Validation: Checking for one of the required response fields...")

        for field in fields:
            if field in content:
                return True
        else:
            logger.error(f"Response doesn't contain any of the requirement fields")
            return False
    
    async def _haveErrors(content: dict) -> bool:
        '''
        Check for errors in the response
        '''
        logger.debug(f"Event Validation: Checking for errors in the response...")

        for field in EventValidator._errorFields:
            if field in content:
                if field == "error":
                    error_code = content[field]["error_code"]
                    error_msg = content[field]["error_msg"]
                    request_params = content[field]["request_params"]
                    
                    if content[field]["error_code"] in [5, 1116]:
                        raise AuthError(error_code, error_msg, request_params)
                    
                    raise VkApiError(error_code, error_msg, request_params)
                
                if field == "failed":
                    failed_code = content[field]
                    raise LongPollError(failed_code, content["ts"] if "ts" in content else None)
                
                return True
            
        else:
            return False

    async def validate(response: ClientResponse,
                       from_polling: bool = False) -> dict:
        '''
        Validating response from API
        '''
        logger.debug(f"Validating event response for [{response.method}] \"{response.url}\"...")

        jsonIsValid = await EventValidator._isJsonValid(response)
        fieldsAreValid = "-"
        haveErrors = "-"
        content = None

        if jsonIsValid:
            content = await response.json()
            
            fieldsAreValid = await EventValidator._fieldsAreValid(content, 
                                                                  EventValidator._requiredFields if not from_polling else EventValidator._pollingRequiredFields)
            haveErrors = await EventValidator._haveErrors(content)

            if fieldsAreValid and not haveErrors:
                logger.debug("Event response is valid")
                return content
        
        logger.warning(f"Event response is not valid")
        logger.warning(f'{"JSON is valid":<15}|{"":>1}{"Fields are valid":<18}|{"":>1}{"Has no errors":<15}|{"":>1}{"content":<15}')
        logger.warning(f'{color(jsonIsValid, indent=15)}|{"":>1}{color(fieldsAreValid, indent=18)}|{"":>1}{color(not haveErrors, indent=15)}|{"":>1}{color(content)}')

        raise EventValidationError(jsonIsValid, fieldsAreValid, content)