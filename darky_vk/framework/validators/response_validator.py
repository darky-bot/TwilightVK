from aiohttp import ClientResponse
from http import HTTPStatus

from ...utils.config_loader import Configuration
from ...logger.darky_logger import DarkyLogger
from ..handlers.exceptions import ValidationError, IsNotSuccessCode

CONFIG = Configuration().get_config()

class ResponseValidator:

    def __init__(self):
        self.required_fields = {
            'response': None,
            'failed': None,
            "error": None,
            "updates": None
        }
        self.logger = DarkyLogger("resp-validator", CONFIG.LOGGER)

    def is_valid(self,
                 response:ClientResponse):
        self.logger.debug("Type matching check...")
        if type(response) != ClientResponse:
            return False
        return True

    async def validate(self,
                 response:ClientResponse) -> dict:

        if not self.is_valid(response):
            self.logger.error("Response is not in valid raw format")
            raise ValidationError(f"Response is not in valid raw format")
        
        self.logger.debug("Checking HTTP Status Code...")
        if response.status != HTTPStatus.OK:
            self.logger.warning(f"HTTP Status code: {response.status}")
            raise IsNotSuccessCode()
        
        self.logger.debug("Getting JSON...")
        content = await response.json()

        self.logger.debug("Checking for one of the required fields...")
        for field in self.required_fields:
            if field in content:
                break
        else:
            raise ValidationError(f"The response does not contain any required fields.")
        
        self.logger.debug("Response is valid")

        return content