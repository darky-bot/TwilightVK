from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from ..methods import VkMethods

class BaseRule:

    def __init__(self, **kwargs):
        '''
        Base rule with base logic
        All child rules should inherit this one with changing check() function's logic

        :param kwargs: Dict of addictional arguments to this function
        :type kwargs: dict
        '''
        self.event: dict = None
        self.methods: "VkMethods" = None
        self.kwargs: dict = kwargs
        self.__parseKwargs__()
    
    def __parseKwargs__(self):
        '''
        Parsing kwargs attribute, allowing to use each item as separate rule's attribute
        '''
        for key, value in self.kwargs.items():
            setattr(self, key, value)
    
    def __getattr__(self, name):
        '''
        Allows to handle errors with parsing
        '''
        if name not in ['event', 'kwargs', 'methods']:
            return getattr(self, self.kwargs[name])
    
    async def __linkVkMethods__(self, methods):
        '''
        Updates the methods attribute so you could make api requests from inside the rule
        '''
        self.methods = methods
    
    async def check(self, event: dict) -> bool:
        '''
        Main function with specific check logic for specific rule.
        It may be different in different rules
        It should always return the boolean as the result
        '''
        pass

    def __and__(self, other: "BaseRule"):
        return AndRule(self, other)
    
    def and_(self, other: "BaseRule"):
        return AndRule(self, other)
    
    def __or__(self, other: "BaseRule"):
        return OrRule(self, other)
    
    def or_(self, other: "BaseRule"):
        return OrRule(self, other)
    
    def __not__(self):
        return NotRule(self)
    
    def not_(self):
        return NotRule(self)


class AndRule(BaseRule):
    
    def __init__(self, *rules: BaseRule):
        '''
        Модификатор AND для комбинирования правил
        '''
        self.rules = rules

    async def check(self, event: dict):
        results = {}

        for rule in self.rules:

            result = await rule.check(event)

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
        self.rules = rules
    
    async def check(self, event: dict):

        for rule in self.rules:

            result = await rule.check(event)

            if isinstance(result, Exception):
                return result
            
            if result is True:
                return True
            
        return False

class NotRule(BaseRule):
    
    def __init__(self, rule: BaseRule):
        '''
        Модификатор NOT для комбинирования правил
        '''
        self.rule = rule
    
    async def check(self, event: dict):

        result = await self.rule.check(event)
        return not result if isinstance(result, bool) else False