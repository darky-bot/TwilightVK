from aiohttp import ClientResponse

from ...utils.config_loader import Configuration
from ...logger.darky_logger import DarkyLogger

CONFIG = Configuration().get_config()

class EventValidator:

    def __init__(self):
        self.__requiredFields__ = {
            'response': None,
            'failed': None,
            "error": None,
            "updates": None
        }
        self.logger = DarkyLogger("event-validator", CONFIG.LOGGER, silent=True)

    async def __jsonIsValid__(self,
                              response:ClientResponse) -> bool:
        ...
    
    async def __fieldsAreValid__(self,
                                 response:ClientResponse) -> bool:
        ...
    
    async def __haveErrors__(self,
                              response:dict) -> ...:
        ...

    async def validate(self,
                 response:ClientResponse) -> dict:
        self.logger.debug(f"Validating event response for [{response.method}] \"{response.url}\"...")

        jsonIsValid = await self.__jsonIsValid__(response)
        fieldsAreValid = await self.__fieldsAreValid__(response)

        content = await response.json()
        return content