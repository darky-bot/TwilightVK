import pytest

import twilight_vk
from twilight_vk.framework.handlers.exceptions import (
    TwilightInitError
)

@pytest.mark.asyncio
async def test_framework_invalid_initialization():
    with pytest.raises(TwilightInitError):
        twilight_vk.TwilightVK()

class MockGetLongPollServer():

    def __init__(self, isSuccess=True):
        self.method = "GET"
        self.url = "https://fakeauth"
        self.headers = {"Content-Type": "application/json"}
        self.is_success = isSuccess

    async def json(self):
        if self.is_success:
            return {
                "response": {
                                "server": "https://fakeserverurl",
                                "key": "fakekey",
                                "ts": 0
                            }
            }
        return {
                    "error": {
                        "error_code": 5,
                        "error_msg": "User authorization failed: invalid access_token (4).",
                        "request_params": [
                            {
                                "key": "access_token",
                                "value": "123"
                            },
                            {
                                "key": "group_id",
                                "value": 123
                            },
                            {
                                "key": "v",
                                "value": "1.234"
                            }
                        ]
                    }
            }

@pytest.mark.asyncio
async def test_botlongpoll_auth_func_failed(caplog, monkeypatch):
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123
    )

    async def fake_getBotLongPollServer():
        fake_response = MockGetLongPollServer(False)
        return await bot.__bot__.eventValidator.validate(fake_response)
    
    monkeypatch.setattr(bot.__bot__.vk_methods.groups, "getLongPollServer", fake_getBotLongPollServer)

    await bot.__bot__.auth()
    assert "Authrization error: [5] User authorization failed: invalid access_token (4)." in caplog.text

@pytest.mark.asyncio
async def test_botlongpoll_auth_func_success(caplog, monkeypatch):
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123
    )

    async def fake_getBotLongPollServer():
        fake_response = fake_response = MockGetLongPollServer(True)
        return await bot.__bot__.eventValidator.validate(fake_response)
    
    monkeypatch.setattr(bot.__bot__.vk_methods.groups, "getLongPollServer", fake_getBotLongPollServer)

    await bot.__bot__.auth()
    assert "Authorized" in caplog.text

@pytest.mark.skip
@pytest.mark.asyncio
async def test_botlongpoll_check_event_func():
    bot: twilight_vk.TwilightVK = get_authorized_bot
    response = await bot.__bot__.check_event()
    assert response.keys() == {"ts": 0, "updates": []}.keys()

@pytest.mark.skip
@pytest.mark.asyncio
async def test_event_handler_rule_true(caplog):
    bot: twilight_vk.TwilightVK = get_authorized_bot
    @bot.on_event.message_new(TextRule(["hello", "hi"], ignore_case=True))
    async def hello_world(event: dict):
        return "Hello world"
    event = {
        {
            "group_id": 123,
            "type": "message_new",
            "event_id": "35f7f1c571580321e613a76cc299dbc1305376e6",
            "v": "5.199",
            "object": {
                "client_info": {
                    "button_actions": [
                        "text",
                        "vkpay",
                        "open_app",
                        "location",
                        "open_link",
                        "open_photo",
                        "callback",
                        "intent_subscribe",
                        "intent_unsubscribe"
                    ],
                    "keyboard": True,
                    "inline_keyboard": True,
                    "carousel": True,
                    "lang_id": 0
                },
                "message": {
                    "date": 1753820182,
                    "from_id": 1,
                    "id": 123,
                    "version": 10059049,
                    "out": 0,
                    "fwd_messages": [],
                    "important": False,
                    "is_hidden": False,
                    "attachments": [],
                    "conversation_message_id": 1,
                    "text": "hi",
                    "peer_id": 1,
                    "random_id": 0
                }
            }
        }
    }
    await bot.__eventHandler__.handle(event)
    assert "hello_world was added to MESSAGE_NEW with rules: ['TextRule']" in caplog.text
    assert "MESSAGE_NEW is working asynchronously right now..." in caplog.text
    assert "Checking rules for hello_world from MESSAGE_NEW..." in caplog.text
    assert "Checking rule TextRule({'value': ['hello', 'hi'], 'ignore_case': True})..." in caplog.text
    assert "Rule TextRule return the True" in caplog.text

@pytest.mark.skip
@pytest.mark.asyncio
async def test_event_handler_rule_false(caplog):
    ...

#TODO: methods tests
#TODO: errors tests