import pytest
import pytest_asyncio

from twilight_vk import TwilightVK
from twilight_vk.utils.types.event_types import BotEventType

@pytest_asyncio.fixture
def bot(_function_event_loop):
    _bot = TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123,
        loop_wrapper=_function_event_loop
    )
    yield _bot


@pytest.fixture
def response():
    return {
        "ts": 123,
        "updates": [
            {
                "type": BotEventType.MESSAGE_TYPING_STATE,
                "object": {
                    "state": "typing",
                    "from_id": 123,
                    "to_id": -123
                }
            },
            {
                "type": BotEventType.MESSAGE_NEW,
                "object": {
                    "client_info": {},
                    "message": {
                        "conversation_message_id": 1,
                        "peer_id": 123,
                        "text": "Test"
                    }
                }
            },
            {
                "type": BotEventType.LIKE_ADD,
                "object": {
                    "liker_id": 123,
                    "object_type": "post",
                    "object_owner_id": 123,
                    "object_id": 1,
                    "thread_reply_id": 1,
                    "post_id": 1
                }
            }
        ]
    }