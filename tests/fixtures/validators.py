from http import HTTPStatus

import pytest

from twilight_vk.utils.types.event_types import BotEventType
from twilight_vk.utils.types.response import Response

class MockedHttpResponse:

    def __init__(self,
                 *args,
                 **kwargs):
        self.status = kwargs.get('status') or HTTPStatus.OK
        self.method = kwargs.get('method') or "GET"
        self.url = "https://api.example.com/get"
        self.response = kwargs.get('response') or {
            "response": {
                "test": 1
            }
        }
        self.headers = kwargs.get('headers') or {"Content-Type": "application/json"}
    
    async def json(self):
        return self.response

class MockEvent:

    def __init__(self,
                 event_type: str):
        self.object = {
            "type": event_type or BotEventType.MESSAGE_NEW,
            "object": {
                "message": {
                    "conversation_message_id": 1,
                    "peer_id": 123,
                    "text": "test"
                }
            }
        }
    
    def get(self):
        return self.object

@pytest.fixture
def http_responses():
    return [
        MockedHttpResponse(
            status = HTTPStatus.OK,
        ),
        MockedHttpResponse(
            status = HTTPStatus.TEMPORARY_REDIRECT
        ),
        MockedHttpResponse(
            status = HTTPStatus.BAD_REQUEST
        )
    ]

@pytest.fixture
def event_responses():
    return [
        MockedHttpResponse(
            headers = {"Content-Type": "application/json"},
            response = {"response": {"test": 1}}
        ),
        MockedHttpResponse(
            headers = {'Invalid-header': 'Blep'},
        ),
        MockedHttpResponse(
            response = {"Invalid-response": "test"}
        ),
        MockedHttpResponse(
            response = {"ts": 0, "updates": []}
        ),
        MockedHttpResponse(
            response = {"failed": 3}
        ),
        MockedHttpResponse(
            response = {
                "error": {
                    "error_code": 1,
                    "error_msg": "Unknown error, try again later",
                    "request_params": [
                        {
                            "key": "v",
                            "value": "1.234"
                        }
                    ]
                }
            }
        )
    ]

@pytest.fixture
def event_responses_results():
    return [
        {"response": {"test": 1}},
        None,
        None,
        {"ts": 0, "updates": []},
        {"failed": 3},
        {
            "error": {
                "error_code": 1,
                "error_msg": "Unknown error, try again later",
                "request_params": [
                    {
                        "key": "v",
                        "value": "1.234"
                    }
                ]
            }
        }
    ]

@pytest.fixture
def request_params():
    return {
        "peer_ids": [123, 456],
        "extended": False,
        "forward": {"is_reply": True},
        "message": "abc-test"
    }

@pytest.fixture
def outputs():
    return [
        (MockEvent(event_type=BotEventType.MESSAGE_NEW).get(), "Test output"),
        (MockEvent(event_type=BotEventType.MESSAGE_NEW).get(), Response(
            peer_ids=[123],
            message="Test output"
        )),
        (MockEvent(event_type=BotEventType.LIKE_ADD).get(), "Test output"),
        (MockEvent(event_type=BotEventType.LIKE_ADD).get(), Response(
            peer_ids=[123],
            message="Test output"
        ))
    ]