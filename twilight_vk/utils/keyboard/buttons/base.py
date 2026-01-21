import logging

from ...types.keyboard_colors import KeyboardColor

logger = logging.getLogger('keyboard')

class KeyboardButton:
    '''
    Keyboard button
    '''
    def __init__(self,
                 type: str = None,
                 label: str = None,
                 payload: str = None,
                 hash: str = None,
                 link: str = None,
                 app_id: int = None,
                 owner_id: int = None,
                 color: str = KeyboardColor.SECONDARY):
        '''
        Базовый класс кнопки для клавиатуры, поддерживающий все параметры для универсальной конфигурации
        (см. https://dev.vk.ru/ru/api/bots/development/keyboard#Типы%20кнопок)
        '''
        self._type: str = type

        self._label: str = None
        self._payload: str = None

        if label:
            if len(label) > 40:
                logger.warning(f"The maximum length of the label is 40 characters. Label will be cut off to the limits")
            self._label: str = f"{label[:37]}..."

        if payload:
            if len(payload) > 255:
                logger.error(f"The maximum length of the payload is 255 characters.")
                raise ValueError("payload's length should be less than 255 characters.")
            self._payload: str = payload

        self._hash: str = hash
        self._link: str = link
        self._app_id: int = app_id
        self._owner_id: int = owner_id

        self._color: str = color

        logger.debug(f"Generating keyboard button's markup with type: {self._type}")
        
        self._button = {
            "action": {
                "type": self._type
            }
        }

        if self._type in ["text", "callback"]:
            self._button.setdefault("color", self._color)

        if self._type in ["text", "callback", "open_link", "open_app"]:
            self._button["action"].setdefault("label", self._label)
        
        if self._payload:
            self._button["action"].setdefault("payload", self._payload)
        
        if (self._type == "vkpay") or (self._type == "open_app" and self._hash):
            self._button["action"].setdefault("hash", self._hash)

        if self._type == "open_link":
            self._button["action"].setdefault("link", self._link)
        
        if self._type == "open_app":
            self._button["action"].setdefault("app_id", self._app_id)
            if self._owner_id:
                self._button["action"].setdefault("owner_id", self._owner_id)
        
        logger.debug(f"Button was successfully generated: {self._button}")

    def getButton(self):
        '''
        Возвращает JSON описывающий кнопку
        '''
        return self._button
