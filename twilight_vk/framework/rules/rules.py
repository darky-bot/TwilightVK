from .base import BaseRule
from ...utils.twiml import TwiML
from ...utils.types.event_types import MessageActionTypes
from ...framework.exceptions.vkapi import VkApiError
from ...utils.types.event_types import BotEventType

class TrueRule(BaseRule):
    
    def __init__(self) -> None:
        '''
        Возвращает всегда True
        Правило сделано в основном для теста
        '''
        super().__init__(
            on_event_types = [BotEventType.__getattribute__(BotEventType, event_type) for event_type in BotEventType.__dict__ if "__" not in event_type]
        )

    async def check(self, event: dict):
        return True

class FalseRule(BaseRule):

    def __init__(self) -> None:
        '''
        Возвращает всегда False
        Правило сделано в основном для теста
        '''
        super().__init__(
            on_event_types = [BotEventType.__getattribute__(BotEventType, event_type) for event_type in BotEventType.__dict__ if "__" not in event_type]
        )

    async def check(self, event: dict):
        return False

class ContainsRule(BaseRule):

    def __init__(self,
                 triggers: str | list[str],
                 ignore_case: bool = False,
                 need_list: bool = True):
        '''
        Проверяет наличие указанных в value фрагментов текста в сообщении, возвращает True при нахождении

        :param triggers: Слова-триггеры
        :type triggers: str | list[str]

        :param ignore_case: Флаг игнорирования регистра
        :type ignore_case: bool

        :param need_list: Дает понять нужно ли возвращать список найденных фрагментов или достаточно просто оповестить
        :type need_list: bool
        '''
        super().__init__()
        self.triggers: list[str] = triggers
        self.ignore_case: bool = ignore_case
        self.need_list: bool = need_list
    
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
        super().__init__()
        self.value: list[str] = value
        self.ignore_case: bool = ignore_case

    async def check(self, event: dict) -> bool:
        text:str = event["object"]["message"]["text"]

        if self.ignore_case:
            text = text.lower()
            self.value = [val.lower() for val in self.value]

        return text in self.value


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
        super().__init__()
        self.value: list[str] = value
        self.ignore_case: bool = ignore_case

    async def check(self, event: dict) -> bool | dict:
        text:str = event["object"]["message"]["text"]
        text = text.lower() if self.ignore_case else text

        twiml = TwiML()

        for _value in self.value:
            _value = _value.lower() if self.ignore_case else _value

            twiml.update_template(_value)
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
        super().__init__()
        self.need_list: bool = need_list
    
    async def _getMentions(self, event: dict) -> dict:
        text: str = event["object"]["message"]["text"]

        twiml = TwiML()
        result = await twiml.extract_mentions(text)

        return result

    async def check(self, event: dict) -> bool | dict:
        result = await self._getMentions(event)

        if result == {"mentions": []}:
            return False
        
        if self.need_list:
            return result
        
        return True

class IsMentionedRule(MentionRule):
    
    '''
    Проверяет был ли упомянут сам бот или нет
    '''
    async def check(self, event: dict) -> bool:
        mentions = await self._getMentions(event)

        if mentions != False:
            for mention in mentions["mentions"]:
                if mention["type"] == "club" and mention["id"] == event.get("group_id", 0):
                    return True
        
        return False


class ReplyRule(BaseRule):

    def __init__(self,
                 callback: bool = True):
        '''
        Проверяет наличие ответа в событии.
        Возвращает True/False в зависимости от результата либо обозначает в переданных параметрах have_reply при callback = True

        :param callback: определяет вывод правила (True/False либо {"have_reply": True}/False)
        :type callback: bool
        '''
        super().__init__()
        self.callback: bool = callback
    
    async def check(self, event: dict) -> bool:
        if event["object"]["message"].get("reply_message", None) is not None:
            if self.callback:
                return {"have_reply": True}
            return True
        return False

class ForwardRule(BaseRule):

    def __init__(self,
                 callback: bool = True):
        '''
        Проверяет наличие пересланного сообщения в событии.
        Возвращает True/False в зависимости от результата либо обозначает в переданных параметрах have_forward при callback = True

        :param callback: определяет вывод правила (True/False либо {"have_forward": True}/False)
        :type callback: bool
        '''
        super().__init__()
        self.callback: bool = callback
    
    async def check(self, event: dict) -> bool:
        if event["object"]["message"].get("fwd_messages") != []:
            if self.callback:
                return {"have_forward": True}
            return True
        return False


class AdminRule(BaseRule):

    def __init__(self) -> None:
        '''
        Проверяет является ли пользователь отправивший сообщение в беседе его администратором
        Возвращает True/False в зависимости от результата
        '''
        super().__init__(
            on_event_types = [BotEventType.MESSAGE_NEW, BotEventType.MESSAGE_EVENT]
        )

    async def _getAdmins(self, event: dict) -> None:
        
        _event_object: dict = event["object"]["message"] if event.get("type") == BotEventType.MESSAGE_NEW else event["object"]
        _peer_id: int = _event_object.get("peer_id")
        _from_id: int = _event_object.get("from_id") if event.get("type") == BotEventType.MESSAGE_NEW else _event_object.get("user_id")

        try:

            event.setdefault("is_admin", None)
            event.setdefault("is_bot_admin", None)

            if (event.get("is_admin") is None or
                event.get("is_bot_admin") is None):

                chat_members = await self.methods.messages.getConversationMembers(
                    peer_id = _peer_id
                )
                
                member: dict
                for member in chat_members["response"]["items"]:

                    _member_id = member.get("member_id")
                    _is_admin = member.get("is_admin", False)

                    if _member_id == _from_id: event["is_admin"] = _is_admin
                    if _member_id == -event.get("group_id"): event["is_bot_admin"] = _is_admin

        except VkApiError as ex:
            
            if ex.error_code == 917:
                event["is_bot_admin"] = False


    async def check(self, event: dict) -> bool:
        await self._getAdmins(event)
        return event.get("is_admin")

class IsAdminRule(AdminRule):

    '''
    Проверяет является ли бот администратором в чате
    Возвращает True/False в зависимости от результата
    '''
    async def check(self, event: dict) -> bool:
        await self._getAdmins(event)
        return event.get("is_bot_admin")


class InvitedRule(BaseRule):
    
    '''
    Возвращает True если какой-либо пользователь был добавлен в чат.
    '''
    async def _whoIsInvited(self, event: dict) -> int:
        if (
            event["object"]["message"].get("action", None) is not None and
            event["object"]["message"]["action"]["type"] == MessageActionTypes.CHAT_INVITE_USER
        ):
            return event["object"]["message"]["action"]["member_id"]
        return 0

    async def check(self, event: dict) -> bool:
        if await self._whoIsInvited(event) != 0:
            return True
        return False 
    
class IsInvitedRule(InvitedRule):

    '''
    Возвращает True если бот был добавлен в чат
    '''
    async def check(self, event: dict) -> bool:
        if await self._whoIsInvited(event) == -event.get("group_id"):
            return True
        return False
    
class OnPayloadRule(BaseRule):
        
    def __init__(self,
                 payload: dict = {}) -> None:
        '''
        Возвращает True если payload совпадает с переданным
        
        :param payload: Ожидаемый payload от события
        :type payload: dict
        '''
        super().__init__(
            on_event_types = [BotEventType.MESSAGE_NEW, BotEventType.MESSAGE_EVENT]
        )
        self.payload: dict = payload
    
    async def check(self, event: dict) -> bool:
        
        _event_object: dict = event["object"]

        if event.get("type") == BotEventType.MESSAGE_NEW: _event_object = event["object"]["message"]

        _payload = _event_object.get("payload", None)

        if self.payload == {} and _payload not in [{}, None]:
            return True
        
        if self.payload == {}: return False
        
        return _payload == self.payload
        
        
