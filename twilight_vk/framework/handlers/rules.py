from ...utils.twiml import TwiML

class BaseRule:

    def __init__(self, **kwargs):
        '''
        Base rule with base logic
        All child rules should inherit this one with changing check() function's logic

        :param kwargs: Dict of addictional arguments to this function
        :type kwargs: dict
        '''
        self.event = None
        self.kwargs = kwargs
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
        if name not in ['event', 'kwargs']:
            return getattr(self, self.kwargs[name])

    async def __updateEvent__(self, event):
        '''
        Updates the event attribute on current one(from the function's argument)
        '''
        self.event = event
    
    async def __earseEvent__(self):
        '''
        Updates the event attribute on empty one, after handling is completed
        '''
        self.event = None
    
    async def check(self) -> bool:
        '''
        Main function with specific check logic for specific rule.
        It may be different in different rules
        It should always return the boolean as the result
        '''
        pass


class TextRule(BaseRule):

    def __init__(self,
                 value:str|list[str],
                 ignore_case:bool=False):
        '''
        Сверяет текст сообщения с указанным, возвращает True при совпадении

        :param value: Ожидаемое значение
        :type value: str | list[str]

        :param ignore_case: Флаг игнорирования регистра
        :type ignore_case: bool
        '''

        self.value = value
        self.ignore_case = ignore_case

    async def check(self) -> bool:
        text:str = self.event["object"]["message"]["text"]
        return (text.lower() if self.ignore_case else text) in \
            ([val.lower() if self.ignore_case else self.value for val in self.value])


class TwiMLRule(BaseRule):

    def __init__(self,
                 value:str|list[str],
                 ignore_case:bool=False):
        '''
        Сверяет текст сообщения с указанным шаблоном на основе regex выражений, 
        возвращает словарь найденных аргументов или False если сообщение не соответствует шаблону

        :param value: Ожидаемое выражение(шаблон)
        :type value: str | list[str]

        :param ignore_case: Флаг игнорирования регистра
        :type ignore_case: bool
        '''

        self.value = value
        self.ignore_case = ignore_case

    async def check(self) -> bool | dict:
        text:str = self.event["object"]["message"]["text"]
        text = text.lower() if self.ignore_case else text

        twiml = TwiML()

        for value in self.value:
            value = value.lower() if self.ignore_case else value

            twiml.update_template(value)
            result = twiml.parse(text)

            if result is not None:
                return result
        else:
            return False