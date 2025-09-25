from typing import TYPE_CHECKING

from .event_handlers import (
    BASE_EVENT_HANDLER,
    DEFAULT_HANDLER,
    MESSAGE_NEW,
    MESSAGE_REPLY
)
from .response_handler import ResponseHandler
from ...utils.event_types import BotEventType

if TYPE_CHECKING:
    from ..methods import VkMethods

class OnEventLabeler:

    def __init__(self, handlers: dict):
        self.handlers = handlers

    def all(self, *rules):
        def decorator(func):
            for handler_name in self.handlers.keys():
                self.handlers[handler_name].__add__(func, rules)
                return func
        return decorator
    
    def message_new(self, *rules):
        def decorator(func):
            self.handlers[BotEventType.MESSAGE_NEW].__add__(func, rules)
            return func
        return decorator

class EventHandler:

    def __init__(self,
                 vk_methods:'VkMethods'):
        self.vk_methods = vk_methods
        self._handlers = {
            "default": DEFAULT_HANDLER(self.vk_methods),
            BotEventType.MESSAGE_NEW: MESSAGE_NEW(self.vk_methods),
            BotEventType.MESSAGE_REPLY: MESSAGE_REPLY(self.vk_methods)
        }
        self.on_event = OnEventLabeler(self._handlers)

    async def handle(self, current_event:dict):
        event_type = current_event.get("type", "default")
        handler:BASE_EVENT_HANDLER = self._handlers.get(event_type, self._handlers["default"])
        await handler.__executeAsync__(current_event)