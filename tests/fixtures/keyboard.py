import pytest

@pytest.fixture
def inline_keyboard_markup():
    return {
        "inline": True,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "TestButton"
                    },
                    "color": "positive"
                }
            ]
        ]
    }

@pytest.fixture
def keyboard_markup():
    return {
        "one_time": True,
        "inline": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "TestButton"
                    },
                    "color": "secondary"
                },
                {
                    "action":{
                        "type":"location",
                        "payload":"{\"button\": \"2\"}"
                    }
                }
            ],
            [
                {
                    "action":{
                        "type":"vkpay",
                        "hash":"action=transfer-to-group&group_id=12345&aid=10"
                    }
                }
            ]
        ]
    }