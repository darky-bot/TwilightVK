from typing import TYPE_CHECKING
from typing import List, Callable

import asyncio

from ...utils.config_loader import Configuration
from ...logger.darky_logger import DarkyLogger
from .rules import *

if TYPE_CHECKING:
    from ..api.methods import VkMethods

CONFIG = Configuration().get_config()

class BASE_EVENT_HANDLER:

    def __init__(self,
                 vk_methods:'VkMethods'):
        self.logger = DarkyLogger(f"event-handler", CONFIG.LOGGER, silent=True)
        self.logger.debug(f"{self.__class__.__name__} event handler is initiated")
        self.vk_methods = vk_methods
        self.__funcs__: List[Callable] = []
    
    def __add__(self, func, rules):
        self.__funcs__.append(
            {
                "rules": rules,
                "func": func
            }
        )
        self.logger.debug(f"{func.__name__} was added to {self.__class__.__name__} "\
                          f"with rules: {[f"{rule.__class__.__name__}" for rule in rules]}")
    
    async def __checkRule__(self, rule, event):
        self.logger.debug(f"Updating event attr in {rule}")
        await rule.__updateEvent__(event)
        self.logger.debug(f"Checking rule {rule.__class__.__name__}({rule.kwargs})...")
        result = await rule.check()
        self.logger.debug(f"Rule {rule.__class__.__name__} returned the {result}")
        return result

    async def __callFunc__(self, handler, event):
        func = handler["func"]
        self.logger.debug(f"Checking rules for {func.__name__} from {self.__class__.__name__}...")
        rule_results = await asyncio.gather(
            *(self.__checkRule__(rule, event) for rule in handler["rules"]),
            return_exceptions=True
        )
        self.logger.debug(f"Rules check results: {rule_results}")
        self.logger.debug(f"{func.__name__}'s rules was checked")
        for rule in rule_results:
            if isinstance(rule, Exception):
                self.logger.warning(f"Got an exception in rules check results. [{rule.__class__.__name__}({rule})]")
                return
            if rule is False:
                self.logger.debug(f"Rule has False value")
                return
        self.logger.debug(f"Calling {func.__name__} from {self.__class__.__name__}...")
        if asyncio.iscoroutinefunction(func):
            response = await func(event)
        else:
            response = func(event)
        await self.__handleOutput__(response, event)
        self.logger.debug(f"{func.__name__} from {self.__class__.__name__} was called")
    
    async def __handleOutput__(self, callback, event):
        if callback:
            if isinstance(callback, str):
                await self.vk_methods.messages.send(peer_ids=event["object"]["message"]["peer_id"], message=callback)
            elif isinstance(callback, type(None)):
                pass
    
    async def __execute__(self, event):
        self.logger.debug(f"{self.__class__.__name__} is working right now...")
        for handler in self.__funcs__:
            await self.__callFunc__(handler, event)
        self.logger.debug(f"{self.__class__.__name__} is finished handling the event")
    
    async def __executeAsync__(self, event):
        self.logger.debug(f"{self.__class__.__name__} is working asynchronously right now...")
        await asyncio.gather(
            *(self.__callFunc__(handler, event) for handler in self.__funcs__),
            return_exceptions=True
        )
        self.logger.debug(f"{self.__class__.__name__} is finished asynchronously handling the event")

class MESSAGE_NEW(BASE_EVENT_HANDLER):
    pass

class MESSAGE_REPLY(BASE_EVENT_HANDLER):
    pass