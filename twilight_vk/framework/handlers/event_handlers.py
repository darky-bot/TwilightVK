from typing import TYPE_CHECKING
from typing import List, Callable

import asyncio

from ...utils.config_loader import Configuration
from ...logger.darky_logger import DarkyLogger
from ..validators.event_validator import EventValidator
from ..validators.http_validator import HttpValidator
from .response import ResponseHandler
from ..exceptions.handler import (
    ResponseHandlerError
)
from ..rules import *

if TYPE_CHECKING:
    from ..methods import VkMethods

CONFIG = Configuration().get_config()

class BASE_EVENT_HANDLER:

    def __init__(self,
                 vk_methods:'VkMethods',):
        '''
        BASE_EVENT_HANDLER is base handler for vk_api events.
        It contsains the base logic for event handler.
        All child event handlers must inherit it

        :param vk_methods: Initialized VkMethods class which allows to use VK API methods
        :type vk_methods: VkMethods
        '''
        self.logger = DarkyLogger(f"event-handler", CONFIG.LOGGER, silent=True)
        self.logger.initdebug(f"{self.__class__.__name__} event handler is initiated")

        self.vk_methods = vk_methods

        self.__funcs__: List[Callable] = []
    
    def __add__(self, 
                func, 
                rules: list):
        '''
        Allows to add callable functions into this handler
        '''
        self.__funcs__.append(
            {
                "rules": rules,
                "func": func
            }
        )
        self.logger.initdebug(f"{func.__name__}() was added to {self.__class__.__name__} "\
                          f"with rules: {[f"{rule.__class__.__name__}" for rule in rules]}")
    
    async def __checkRule__(self,
                            rule: BaseRule, 
                            event: dict):
        '''
        Checking rule result for current function and event
        '''
        self.logger.debug(f"Checking rule {rule.__class__.__name__}({rule.__dict__})...")

        if not hasattr(rule, "methods") or rule.methods is None:
            self.logger.debug(f"Linking VkMethods class to the {rule.__class__.__name__}...")
            await rule.__linkVkMethods__(self.vk_methods)
        
        self.logger.debug(f"Executing {rule.__class__.__name__}.check()")
        result = await rule.check(event)

        self.logger.debug(f"Rule {rule.__class__.__name__} returned the {result}")

        return result

    async def __checkRules__(self, func, handler, event):
        '''
        Checks all results
        '''
        self.logger.debug(f"Checking rules for {func.__name__} from {self.__class__.__name__}...")
        rule_results = await asyncio.gather(
            *(self.__checkRule__(rule, event) for rule in handler["rules"]),
            return_exceptions=True
        )
        self.logger.debug(f"Rules check results: {rule_results}")
        self.logger.debug(f"{func.__name__}'s rules was checked")

        should_stop = False

        for rule in rule_results:
            if isinstance(rule, Exception):
                self.logger.error(f"Got an exception in rules check results. [{rule.__class__.__name__}({rule})]")
                should_stop = True
            if rule is False:
                self.logger.debug(f"One of the rules has returned False")
                should_stop = True

        if should_stop:
            return False
        
        return rule_results
    
    async def __extractArgs__(self, rule_results:list):
        '''
        Extracts all args from rule_results after regex rules
        '''
        args = {}
        if isinstance(rule_results, list):
            for result in rule_results:
                if isinstance(result, dict):
                    for key, value in result.items():
                        args.setdefault(key, value)
        return args
   
    async def __handleOutput__(self,
                               func,
                               callback:str|ResponseHandler,
                               event):
        '''
        Handles the output from functions which was added to handler

        :param callback: Function's output
        :type callback: str | ResponseHandler
        '''
        self.logger.debug(f"Handling response for {self.__class__.__name__}.{func.__name__}...")
        if callback:
            if isinstance(callback, str):
                callback = ResponseHandler(
                    peer_ids=event["object"]["message"]["peer_id"],
                    message=callback,
                    forward={
                        "peer_id": event["object"]["message"]["peer_id"],
                        "conversation_message_ids": event["object"]["message"]["conversation_message_id"],
                        "is_reply": True
                    }
                )
            if isinstance(callback, ResponseHandler):
                response = await self.vk_methods.messages.send(**callback.getData())
                return response
            if isinstance(callback, None):
                return True
        raise ResponseHandlerError(callback)
        
    async def __callFunc__(self, handler:dict, event:dict):
        '''
        Executes separate function from self.__funcs__ list
        '''
        func = handler["func"]

        rule_results = await self.__checkRules__(func, handler, event)

        extracted_args = await self.__extractArgs__(rule_results)
        
        if rule_results is not False:
            self.logger.debug(f"Calling {func.__name__} from {self.__class__.__name__}...")
            if asyncio.iscoroutinefunction(func):
                response = await func(event, **extracted_args)
            else:
                response = func(event, **extracted_args)

            result = await self.__handleOutput__(func, response, event)
            if result:
                self.logger.debug(f"{func.__name__} from {self.__class__.__name__} was called")

    async def __execute__(self, event):
        '''
        Handles the event synchronously
        '''
        self.logger.debug(f"{self.__class__.__name__} is working right now...")
        for handler in self.__funcs__:
            await self.__callFunc__(handler, event)
        self.logger.debug(f"{self.__class__.__name__} is finished handling the event")
    
    async def __executeAsync__(self, event):
        '''
        Handles the event asynchronously
        '''
        self.logger.debug(f"{self.__class__.__name__} is working asynchronously right now...")
        await asyncio.gather(
            *(self.__callFunc__(handler, event) for handler in self.__funcs__),
            return_exceptions=False
        )
        self.logger.debug(f"{self.__class__.__name__} is finished asynchronously handling the event")


class DEFAULT_HANDLER(BASE_EVENT_HANDLER):
    pass

class MESSAGE_NEW(BASE_EVENT_HANDLER):
    pass

class MESSAGE_REPLY(BASE_EVENT_HANDLER):
    pass