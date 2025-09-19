import pytest

from twilight_vk.utils.twiml import TwiML

@pytest.fixture
def twiml():
    twimlInstance = TwiML()
    yield twimlInstance

@pytest.fixture
def data():
    return {
        "messages": [
            "",
            "test",
            "test 123",
            "test darky",
            "test darky 21",
            "test darky darky",
            "test darky abc efg"
        ],
        "templates": [
            "test",
            "test <user>",
            "test <user:int>",
            "test <user:word>",
            "test <user:word> <age:int>",
            "test <user> <testword:word>"
        ],
        "results": [
            [None, {}, {}, {}, {}, {}, {}],
            [None, None, {"user": "123"}, {"user": "darky"}, {"user": "darky 21"}, {"user": "darky darky"}, {"user": "darky abc efg"}],
            [None, None, {"user": 123}, None, None, None, None],
            [None, None, {"user": "123"}, {"user": "darky"}, {"user": "darky"}, {"user": "darky"}, {"user": "darky"}],
            [None, None, None, None, {"user": "darky", "age": 21}, None, None],
            [None, None, None, None, {"user": "darky", "testword": "21"}, {"user": "darky", "testword": "darky"}, {"user": "darky abc", "testword": "efg"}]
        ]
    }

@pytest.mark.asyncio
async def test_parse(twiml: TwiML, data: dict):
    for _temp in range(6):
        twiml.update_template(data.get("templates")[_temp])
        for _msg in range(7):
            result = await twiml.parse(data.get("messages")[_msg])
            assert result == data.get("results")[_temp][_msg]

@pytest.mark.skip("Not ready")
@pytest.mark.asyncio
async def test_extract_mentions_func(twiml: TwiML, data: dict):
    pass