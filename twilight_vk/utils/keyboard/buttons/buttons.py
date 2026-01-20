import logging

from .base import KeyboardButton
from ...types.keyboard_colors import KeyboardColor

logger = logging.getLogger('keyboard')

class TextActionKeyboardButton(KeyboardButton):
    '''
    Кнопка, которая отправляет сообщение с текстом в Label
    (см. https://dev.vk.ru/ru/api/bots/development/keyboard#text)
    '''
    def __init__(self,
                 label: str = None,
                 payload: str = None,
                 color: str = KeyboardColor.SECONDARY):
        super().__init__(
            type = "text",
            label = label,
            payload = payload,
            color = color
        )

class LocationKeyboardButton(KeyboardButton):
    '''
    Кнопка, которая открывает окно с информацией о местоположении
    (см. https://dev.vk.ru/ru/api/bots/development/keyboard#location)
    '''
    def __init__(self,
                 payload: str = None):
        super().__init__(
            type = "location",
            payload = payload
        )

class VkPayKeyboardButton(KeyboardButton):
    '''
    Кнопка, которая открывает окно оплаты VK Pay с предопределенными параметрами
    (см. https://dev.vk.ru/ru/api/bots/development/keyboard#vkpay)
    '''
    def __init__(self,
                 hash: str = None,
                 payload: str = None):
        super().__init__(
            type = "vkpay",
            hash = hash,
            payload = payload
        )

class OpenLinkKeyboardButton(KeyboardButton):
    '''
    Кнопка, которая открывает окно оплаты VK Pay с предопределенными параметрами
    (см. https://dev.vk.ru/ru/api/bots/development/keyboard#open_link)
    '''
    def __init__(self,
                 link: str = None,
                 label: str = None,
                 payload: str = None):
        super().__init__(
            type = "open_link",
            link = link,
            label = label,
            payload = payload
        )

class OpenAppKeyboardButton(KeyboardButton):
    '''
    Кнопка, которая открывает окно оплаты VK Pay с предопределенными параметрами
    (см. https://dev.vk.ru/ru/api/bots/development/keyboard#open_app)
    '''
    def __init__(self,
                 app_id: int = None,
                 label: str = None,
                 owner_id: int = None,
                 hash: str = None,
                 payload: str = None):
        super().__init__(
            type = "open_app",
            app_id = app_id,
            label = label,
            owner_id = owner_id,
            hash = hash,
            payload = payload
        )

class CallbackActionKeyboardButton(KeyboardButton):
    '''
    Кнопка, которая открывает окно оплаты VK Pay с предопределенными параметрами
    (см. https://dev.vk.ru/ru/api/bots/development/keyboard#callback)
    '''
    def __init__(self,
                 label: str = None,
                 payload: str = None,
                 color: str = KeyboardColor.SECONDARY):
        super().__init__(
            type = "callback",
            label = label,
            payload = payload,
            color = color
        )