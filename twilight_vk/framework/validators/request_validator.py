import json
import logging
from typing import Any

from ...utils.keyboard.keyboard import KeyboardMarkup

logger = logging.getLogger('reqst-validator')

class RequestValidator:

    async def _getValidValue(value: 'Any') -> 'Any':
        '''
        Преобразует значение Python в корректное значение для запроса в API
        '''
        logger.debug(f"Validating value: {value} with type: {type(value)}")
        if isinstance(value, bool):
            return "true" if value == True else "false"
        
        if isinstance(value, dict):
            return json.dumps(value)

        if isinstance(value, list):
            return ",".join(value)
        
        if isinstance(value, str):
            return f"{value}"
        
        if isinstance(value, int) or isinstance(value, float):
            return value
        
        if isinstance(value, KeyboardMarkup):
            return json.dumps(value.getMarkup())

        return None

    async def validate(values: dict) -> dict:
        _validValues = {}

        logger.debug(f"Validating request parameters...")
        logger.debug(f"Parameters to validate: {values}")

        for key, value in values.items():
            if value not in ['', None]:
                _validValues.setdefault(key, await RequestValidator._getValidValue(value))

        logger.debug(f"Parameters has been validated. Result: {_validValues}")

        return _validValues