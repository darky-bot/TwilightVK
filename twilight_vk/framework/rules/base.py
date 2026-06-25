from typing import TYPE_CHECKING
from typing import Any
import logging

from ...utils.config import CONFIG
from ...utils.types.event_types import BotEventType

if TYPE_CHECKING:
    from ..methods import VkMethods

logger = logging.getLogger("rule-handler")

class BaseRule:

    def __init__(self, on_event_types: list[str] = [BotEventType.MESSAGE_NEW], **kwargs):
        '''
        Base rule with base logic
        All child rules should inherit this one with changing check() function's logic

        :param on_event_types: Defines on which event type rule could be applied (On default [MESSAGE_NEW])
        :type on_event_types: list[str]

        :param kwargs: Dict of addictional arguments to this function
        :type kwargs: dict
        '''
        self.event: dict = None
        self.methods: "VkMethods" = None
        self.kwargs: dict = kwargs
        self.allowed_event_types: list[str] = on_event_types
        self._parseKwargs()
        logger.debug(f"Rule {self.__class__.__name__}({", ".join(self._printKwargs())}) is initiated")
    
    def _parseKwargs(self):
        '''
        Parsing kwargs attribute, allowing to use each item as separate rule's attribute
        '''
        for key, value in self.kwargs.items():
            setattr(self, key, value)
    
    def _printKwargs(self):
        output = []
        for key, value in self.kwargs.items():
            if key in ["rules", "rule"]:
                output.append(f"{key}: {", ".join(obj.__class__.__name__ for obj in value)}")
                continue
            output.append(f"{key}: {value}")
        return output

    def __getattr__(self, name):
        '''
        Allows to handle errors with parsing
        '''
        if name not in ['event', 'kwargs', 'methods', 'logger']:
            return getattr(self, self.kwargs[name])
    
    async def updateVkMethods(self, methods):
        '''
        Updates the methods attribute so you could make api requests from inside the rule
        '''
        try:
            logger.debug(f"Linking VkMethods class to the {self.__class__.__name__}...")
            self.methods = methods
        except Exception as ex:
            logger.error(f"Got an error while linking", exc_info=True)
            return False
    
    async def _check(self, event: dict, methods: 'VkMethods') -> bool | dict:
        '''
        The shell for Rule.check()
        Allows to logging
        '''
        try:
            logger.debug(f"Checking rule {self.__class__.__name__}({self._printKwargs()})...")

            if event.get("type", None) not in self.allowed_event_types:
                logger.warning(f"Rule {self.__class__.__name__} cannot be applied on non {self.allowed_event_types} event types")
                return False

            if self.methods is None:
                await self.updateVkMethods(methods)
                
            response = await self.check(event)
            logger.debug(f"Rule {self.__class__.__name__} returned {response}")
            return response
        except Exception as ex:
            logger.error(f"Rule {self.__class__.__name__} returned an exception", exc_info=True)
            return False

    async def check(self, event: dict) -> bool | dict:
        '''
        Main function with specific check logic for specific rule.
        It may be different in different rules
        It should always return the boolean as the result
        '''
        pass

    def __and__(self, other: "BaseRule"):
        return AndRule(self, other)
    
    def __or__(self, other: "BaseRule"):
        return OrRule(self, other)
    
    def __invert__(self):
        return NotRule(self)


class AndRule(BaseRule):
    
    def __init__(self, *rules: BaseRule):
        '''
        Модификатор AND для комбинирования правил
        '''
        super().__init__(
            rules = rules
        )

    async def check(self, event: dict):
        results = {}

        rule: BaseRule

        for rule in self.rules:

            result = await rule._check(event, self.methods)

            if isinstance(result, Exception):
                return result
            
            if result is False:
                return False
            
            if isinstance(result, dict):
                results.update(result)

        if results != {}:
            return results
        
        return True

class OrRule(BaseRule):
    
    def __init__(self, *rules: BaseRule):
        '''
        Модификатор OR для комбинирования правил
        '''
        super().__init__(
            rules = rules
        )
    
    async def check(self, event: dict):

        rule: BaseRule

        for rule in self.rules:

            result = await rule._check(event, self.methods)

            if isinstance(result, Exception):
                return result
            
            if isinstance(result, dict):
                return result
            
            if result is True:
                return True
            
        return False

class NotRule(BaseRule):
    
    def __init__(self, rule: BaseRule):
        '''
        Модификатор NOT для комбинирования правил
        '''
        super().__init__(
            rules = (rule,)
        )
    
    async def check(self, event: dict):

        rule: BaseRule

        for rule in self.rules:

            result = await rule._check(event, self.methods)
            
            return not result if isinstance(result, bool) else False