import pytest

from twilight_vk.framework.rules import *
from twilight_vk.framework.handlers.event_handlers import DEFAULT_HANDLER

@pytest.fixture()
def fake_event():
    return {
        "group_id": 123,
        "type": "message_new",
        "object": {
            "client_info": {},
            "message": {
                "from_id": 1234,
                "id": 1,
                "reply_message": {},
                "fwd_messages": [],
                "attachments": [],
                "conversation_message_id": 1,
                "text": "",
                "peer_id": 2000000001
            }
        }
    }

@pytest.fixture()
def messages_list():
    return [
        "test",
        "test darky",
        "test test",
        "test [club123|@club123]",
        "[club123|@club123]",
        "[club123|@club123] test",
        "test [id1234|@id1234]",
        "[id1234|@id1234]",
        "[id1234|@id1234] test",
        "darky",
        "test [club123|@club123] [id1234|@id1234] darky"
    ]

@pytest.fixture()
def results():
    return [
        [True, False, {"triggers": ["test"]}, True, False, False, False],
        [True, False, {"triggers": ["test", "darky"]}, True, {"variable": "darky"}, False, False],
        [True, False, {"triggers": ["test"]}, False, {"variable": "test"}, False, False],
        [True, False, {"triggers": ["test"]}, False, {"variable": "[club123|@club123]"}, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]}, True],
        [True, False, False, False, False, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]}, True],
        [True, False, {"triggers": ["test"]}, False, False, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]}, True],
        [True, False, {"triggers": ["test"]}, False, {"variable": "[id1234|@id1234]"}, {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, False],
        [True, False, False, False, False, {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, False],
        [True, False, {"triggers": ["test"]}, False, False, {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, False],
        [True, False, {"triggers": ["darky"]}, False, False, False, False],
        [True, False, {"triggers": ["test", "darky"]}, False, {"variable": "[club123|@club123] [id1234|@id1234] darky"}, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}, {"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, True]
    ]

@pytest.fixture
def handler_results():
    return [
        {"triggers": ["test"]},
        {
            "triggers": ["test", "darky"],
            "variable": "darky"
        },
        {
            "triggers": ["test"],
            "variable": "test"
        },
        {
            "triggers": ["test"],
            "variable": "[club123|@club123]",
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]
        },
        {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]},
        {
            "triggers": ["test"],
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]
        },
        {
            "triggers": ["test"],
            "variable": "[id1234|@id1234]",
            "mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]
        },
        {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]},
        {
            "triggers": ["test"],
            "mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]
        },
        {"triggers": ["darky"]},
        {
            "triggers": ["test", "darky"],
            "variable": "[club123|@club123] [id1234|@id1234] darky",
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}, 
                         {"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]
        }
    ]

@pytest.fixture()
def rules_list():
    return [
        TrueRule(),
        FalseRule(),
        ContainsRule(triggers=["test", "darky"], ignore_case=True),
        TextRule(value=["test", "test darky"], ignore_case=True),
        TwiMLRule(value=["test <variable>"], ignore_case=True),
        MentionRule(),
        IsMentionedRule()
    ]

class MockVkMethods:

    def __init__(self):
        pass

@pytest.mark.asyncio
async def test_rules(fake_event: dict, messages_list: list, results: list, rules_list: list[BaseRule]):
    for test in range(len(messages_list)):
        fake_event["object"]["message"]["text"] = messages_list[test]
        rule_results = [await rule.check(fake_event) for rule in rules_list]
        assert rule_results == results[test]

@pytest.mark.asyncio
async def test_handlerRulesInput(fake_event: dict, messages_list: list, results: list, rules_list: list[BaseRule], handler_results: list):
    for test in range(len(messages_list)):
        fake_event["object"]["message"]["text"] = messages_list[test]
        rule_results = [await rule.check(fake_event) for rule in rules_list]
        handler_result = await DEFAULT_HANDLER(MockVkMethods()).__extractArgs__(rule_results)
        assert handler_result == handler_results[test]