from .base import BaseRule
from ...utils.twiml import TwiML

class TrueRule(BaseRule):

    '''
    Возвращает всегда True
    Правило сделано в основном для теста
    '''
    async def check(self, event: dict):
        return True

class FalseRule(BaseRule):

    '''
    Возвращает всегда False
    Правило сделано в основном для теста
    '''
    async def check(self, event: dict):
        return False

class TriggerRule(BaseRule):

    def __init__(self,
                 triggers: str | list[str],
                 ignore_case: bool = False,
                 need_list: bool = True):
        '''
        Проверяет наличие указанных в value фрагментов текста(триггеров) в сообщении, возвращает True при нахождении

        :param triggers: Слова-триггеры
        :type triggers: str | list[str]

        :param ignore_case: Флаг игнорирования регистра
        :type ignore_case: bool

        :param need_list: Дает понять нужно ли возвращать список сработанных триггеров или достаточно просто оповестить
        :type need_list: bool
        '''
        super().__init__(
            triggers = triggers,
            ignore_case = ignore_case,
            need_list = need_list
        )
    
    async def check(self, event: dict) -> bool | dict:
        text: str = event["object"]["message"]["text"]
        text = text.lower() if self.ignore_case else text
        result = {
            "triggers": []
        }

        for trigger in self.triggers:
            if trigger in text:
                if self.need_list:
                    result["triggers"].append(trigger)
                    continue
                return True
            
        if result["triggers"] != []:
            return result
        
        return False


class TextRule(BaseRule):

    def __init__(self,
                 value: str | list[str],
                 ignore_case: bool = False):
        '''
        Сверяет текст сообщения с указанным, возвращает True при совпадении

        :param value: Ожидаемое значение
        :type value: str | list[str]

        :param ignore_case: Флаг игнорирования регистра
        :type ignore_case: bool
        '''

        super().__init__(
            value = value,
            ignore_case = ignore_case
        )

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

        super().__init__(
            value = value,
            ignore_case = ignore_case
        )

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

    def __init__(self,
                 need_list: bool = True):
        '''
        Проверяет наличие упоминаний в сообщении
        возвращает словарь найденных упоминаний/True или False если ни одного упоминания не было в сообщении
        
        :param need_list: Дает понять нужно ли возвращать список упоминаний или достаточно просто оповестить что упоминание было
        :type need_list: bool
        '''
        super().__init__(
            need_list = need_list
        )

    async def check(self, event: dict) -> bool | dict:
        text: str = event["object"]["message"]["text"]

        twiml = TwiML()
        result = await twiml.extract_mentions(text)

        if result == {"mentions": []}:
            return False
        
        if self.need_list:
            return result
        
        return True

class IsMentionedRule(BaseRule):
    
    '''
    Проверяет был ли упомянут сам бот или нет
    '''
    async def check(self, event: dict) -> bool:
        _mentions = MentionRule()
        mentions = await _mentions.check(event)

        if mentions != False:
            for mention in mentions["mentions"]:
                if mention["type"] == "club" and mention["id"] == event.get("group_id", 0):
                    return True
        
        return False


class ReplyRule(BaseRule):
    pass

class ForwardRule(BaseRule):
    pass


class IsBotAdminRule(BaseRule):

    def __init__(self):
        '''
        Проверяет является ли бот администратором в чате
        Возвращает True/False в зависимости от результата
        '''
        super().__init__(

        )

    async def check(self, event: dict) -> bool:
        pass

class IsAdminRule(BaseRule):

    def __init__(self):
        '''
        Проверяет является ли пользователь отправивший сообщение в беседе его администратором.
        Возвращает True/False в зависимости от результата
        '''
        super().__init__(
            
        )

    async def check(self, event: dict) -> bool:
        pass