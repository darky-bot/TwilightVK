import asyncio

import pytest
import pytest_asyncio
from aiohttp import ClientResponse

from twilight_vk import TwilightVK

@pytest_asyncio.fixture
def bot(_function_event_loop):
    _bot = TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123,
        loop_wrapper=_function_event_loop
    )
    yield _bot

class MockEventGenerator:

    def __init__(self,
                 event_type: str = "default"):
        self.method = "GET"
        self.url = "https://api.example.com/"
        self.headers = {"Content-Type": "application/json"}
        self.body = {}

        match event_type:
            
            case "default":
                self.body = {
                    "ts": 123,
                    "updates": []
                }
        
            case "auth success":
                self.body = {
                    "response": {
                        "server": self.url,
                        "key": "fakekey123",
                        "ts": 123
                    }
                }
        
            case "auth fail":
                self.body = {
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
            
            case "message_typing_state":
                self.body = {
                    "ts": 123,
                    "updates": [
                        {
                            "group_id": 123,
                            "type": "message_typing_state",
                            "object": {
                                "from_id": 123,
                                "to_id": -123,
                                "state": "typing"
                            }
                        }
                    ]
                }

            case "message_new":
                self.body = {
                    "ts": 123,
                    "updates": [
                        {
                            "group_id": 123,
                            "type": "message_new",
                            "object": {
                                "client_info": {},
                                "message": {
                                    "from_id": 123,
                                    "id": 1,
                                    "conversation_message_id": 1,
                                    "text": "a",
                                    "peer_id": 2000000001
                                }
                            }
                        }
                    ]
                }
            
            case "like_add":
                self.body = {
                    "ts": 123,
                    "updates": [
                        {
                            "group_id": 123,
                            "type": "like_add",
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
            
            case "failed event 1":
                self.body = {
                    "failed": 1,
                    "ts": 321
                }
            
            case "failed event 2":
                self.body = {
                    "failed": 2
                }

            case "failed event 3":
                self.body = {
                    "failed": 3
                }
        
    async def json(self):
        return self.body
    
    async def get(self, *args, **kwargs):
        return self