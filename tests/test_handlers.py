import pytest
import twilight_vk

@pytest.mark.skip("Not ready")
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

@pytest.mark.skip("Not ready")
@pytest.mark.asyncio
async def test_event_handler_rule_false(caplog):
    ...