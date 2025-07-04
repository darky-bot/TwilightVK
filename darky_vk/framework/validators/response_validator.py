from aiohttp import ClientResponse
from http import HTTPStatus

from ..handlers.exceptions import ValidationError, IsNotSuccessCode

class ResponseValidator:

    def __init__(self):
        self.required_fields = {
            'response': None,
            'failed': None,
            "error": None
        }

    def is_valid(self,
                 response:ClientResponse):
        if type(response) != ClientResponse:
            return False
        return True

    async def validate(self,
                 response:ClientResponse) -> dict:

        if not self.is_valid(response):
            raise ValidationError(f"Response is not in valid raw format")
        
        if response.status != HTTPStatus.OK:
            raise IsNotSuccessCode()
        
        content = await response.json()

        for field in self.required_fields:
            if field in content:
                break
        else:
            raise ValidationError(f"The response does not contain any required fields.")
        
        return content