from .base import BaseRule
from ...utils.twiml import TwiML

class TrueRule(BaseRule):

    def __init__(self):
        '''
        Возвращает всегда True
        Правило сделано в основном для теста
        '''
        pass

    async def check(self, event: dict):
        return True

class FalseRule(BaseRule):

    def __init__(self):
        '''
        Возвращает всегда False
        Правило сделано в основном для теста
        '''
        pass

    async def check(self, event: dict):
        return False

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

    async def check(self, event: dict) -> bool:
        text:str = event["object"]["message"]["text"]
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

    async def check(self, event: dict) -> bool | dict:
        text:str = event["object"]["message"]["text"]
        text = text.lower() if self.ignore_case else text

        twiml = TwiML()

        for value in self.value:
            value = value.lower() if self.ignore_case else value

            twiml.update_template(value)
            result = await twiml.parse(text)

            if result is not None:
                return result
        else:
            return False


class MentionRule(BaseRule):

    def __init__(self):
        '''
        Проверяет наличие упоминаний в сообщении
        возвращает словарь найденных упоминаний или False если ни одного упоминания не было в сообщении
        '''
        pass

    async def check(self, event: dict):
        pass

class ReplyRule(BaseRule):
    pass

class ForwardRule(BaseRule):
    pass


class IsAdminRule(BaseRule):

    def __init__(self):
        '''
        Проверяет является ли пользователь отправивший сообщение в беседе его администратором.
        Возвращает True/False в зависимости от результата
        '''
        pass

    async def check(self, event: dict) -> bool:
        pass