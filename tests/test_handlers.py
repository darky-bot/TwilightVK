import pytest
import asyncio

from twilight_vk import TwilightVK
from twilight_vk.framework.rules import TrueRule
from twilight_vk.framework.exceptions.framework import FrameworkError
from twilight_vk.framework.handlers.events import BotEventType

@pytest.fixture
def bot():
    botInst = TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123
    )
    return botInst

class MockPolling:

    def get() -> dict:
        return {
                    "group_id": 123,
                    "type": "message_new",
                    "object": {
                        "client_info": {},
                        "message": {
                            "from_id": 123,
                            "text": "abc"
                        }
                    }
                }
    
@pytest.mark.asyncio
async def test_messagenew_handler(bot: TwilightVK, monkeypatch):
    
    @bot.on_event.message_new(TrueRule())
    async def handle(event: dict):
        return "OK"
    
    async def fake_outputHandler(func, callback, event):
        assert True
    
    monkeypatch.setattr(bot.__bot__.event_handler._handlers[BotEventType.MESSAGE_NEW], "__handleOutput__", fake_outputHandler)
    
    results = await asyncio.gather(
        bot.__bot__.event_handler.handle(MockPolling.get()),
        return_exceptions=True
    )
    for result in results:
        assert isinstance(result, Exception) == False