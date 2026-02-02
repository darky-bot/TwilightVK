import asyncio

import pytest
import pytest_asyncio

from twilight_vk import TwilightVK
from twilight_vk.framework.rules import TrueRule
from twilight_vk.utils.types.event_types import BotEventType
from tests.fixtures.handlers import (
    bot,
    response
)

@pytest.mark.asyncio
async def test_labeler(bot: TwilightVK, caplog):
    
    @bot.on_event.all(TrueRule())
    async def foo(event: dict):
        return "OK"
    
    for handler_name in bot.__bot__._router._handlers.keys():
        assert bot.__bot__._router._handlers[handler_name]._funcs[0].get("func", False) == foo
        assert isinstance(bot.__bot__._router._handlers[handler_name]._funcs[0].get("rules")[0], TrueRule)

@pytest.mark.asyncio
async def test_event_handlers(bot: TwilightVK, caplog, monkeypatch, response: dict):
    
    @bot.on_event.message_new(TrueRule())
    async def handle_message(event: dict):
        assert isinstance(event, dict)
        assert event.keys() == {"type": "test", "object": {}}.keys()
        assert event["object"].keys() == {"client_info": {}, "message": {}}.keys()
        bot.logger.info(f"TEST_MESSAGE_NEW")
    
    @bot.on_event.raw(BotEventType.LIKE_ADD)
    async def handle_like(event: dict):
        assert isinstance(event, dict)
        assert event.keys() == {"type": "test", "object": {}}.keys()
        assert event["object"].keys() == {
            "liker_id": 123,
            "object_type": "post",
            "object_owner_id": 123,
            "object_id": 1,
            "thread_reply_id": 1,
            "post_id": 1
        }.keys()
        bot.logger.info(f"TEST_LIKE_ADD")

    async def fake_messageSend(*args, **kwargs):
        return True

    for handler_name in bot.__bot__._router._handlers.keys():
        monkeypatch.setattr(bot.__bot__._router._handlers[handler_name].vk_methods.messages, "send", fake_messageSend)

    results = await asyncio.gather(
        *(bot.__bot__._router.route(event) for event in response["updates"]),
        return_exceptions=False
    )

    for result in results:

        if result is None:
            assert True
            continue

        assert result
    
    assert "TEST_MESSAGE_NEW" in caplog.text
    assert "TEST_LIKE_ADD" in caplog.text