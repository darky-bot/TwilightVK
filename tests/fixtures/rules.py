import pytest

from twilight_vk.framework.rules import *

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
    return {
        "messages": [
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
        ],
        "replies": [
            None,
            {"test": "message"},
            None,
            None,
            {"test": "message"},
            None,
            None,
            {"test": "message"},
            None,
            None,
            {"test": "message"}
        ],
        "fwds": [
            [],
            [],
            [{"test": "message"}],
            [],
            [],
            [{"test": "message"}],
            [],
            [],
            [{"test": "message"}],
            [],
            []
        ],
        "actions": [
            None,
            {"type": "chat_invite_user", "member_id": 1234},
            {"type": "chat_invite_user", "member_id": -123},
            None,
            {"type": "chat_invite_user", "member_id": 1234},
            {"type": "chat_invite_user", "member_id": -123},
            None,
            {"type": "chat_invite_user", "member_id": 123},
            {"type": "chat_invite_user", "member_id": -123},
            None,
            {"type": "chat_invite_user", "member_id": 123}
        ],
        "payloads": [
            None,
            {},
            {"payload": "test"},
            {"test": 123},
            {"test": "test"},
            {"test": "payload"}
        ]
    }

@pytest.fixture()
def logic_rules_results():
    return [
        True,
        False,
        True,
        False,
        False,
        True,
        True,
        False,
        True,
        True,
        {"triggers": ["darky"]},
        False,
        {"triggers": ["darky"]},
        False,
        {"triggers": ["darky"]},
        {"triggers": ["darky"], "text": "darky pony"}
    ]

@pytest.fixture()
def results():
    return [
        [True, False, {"triggers": ["test"]}, True, False, False, False, False, False, False, True, False, False],
        [True, False, {"triggers": ["test", "darky"]}, True, {"variable": "darky"}, False, False, {"have_reply": True}, False, False, True, True, False],
        [True, False, {"triggers": ["test"]}, False, {"variable": "test"}, False, False, False, {"have_forward": True}, False, True, True, True],
        [True, False, {"triggers": ["test"]}, False, {"variable": "[club123|@club123]"}, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]}, True, False, False, False, True, False, False],
        [True, False, False, False, False, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]}, True, {"have_reply": True}, False, False, True, True, False],
        [True, False, {"triggers": ["test"]}, False, False, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]}, True, False, {"have_forward": True}, False, True, True, True],
        [True, False, {"triggers": ["test"]}, False, {"variable": "[id1234|@id1234]"}, {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, False, False, False, False, True, False, False],
        [True, False, False, False, False, {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, False, {"have_reply": True}, False, False, True, True, False],
        [True, False, {"triggers": ["test"]}, False, False, {"mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, False, False, {"have_forward": True}, False, True, True, True],
        [True, False, {"triggers": ["darky"]}, False, False, False, False, False, False, False, True, False, False],
        [True, False, {"triggers": ["test", "darky"]}, False, {"variable": "[club123|@club123] [id1234|@id1234] darky"}, {"mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}, {"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]}, True, {"have_reply": True}, False, False, True, True, False]
    ]

@pytest.fixture()
def non_message_new_results():
    return [
        [True, False, False, False, False, False, False, False, False, False, False, False, False]
    ]

@pytest.fixture
def handler_results():
    return [
        {"triggers": ["test"]},
        {
            "triggers": ["test", "darky"],
            "variable": "darky",
            "have_reply": True
        },
        {
            "triggers": ["test"],
            "variable": "test",
            "have_forward": True
        },
        {
            "triggers": ["test"],
            "variable": "[club123|@club123]",
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}]
        },
        {
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}],
            "have_reply": True
        },
        {
            "triggers": ["test"],
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}],
            "have_forward": True
        },
        {
            "triggers": ["test"],
            "variable": "[id1234|@id1234]",
            "mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}]
        },
        {
            "mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}],
            "have_reply": True
        },
        {
            "triggers": ["test"],
            "mentions": [{"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}],
            "have_forward": True
        },
        {"triggers": ["darky"]},
        {
            "triggers": ["test", "darky"],
            "variable": "[club123|@club123] [id1234|@id1234] darky",
            "mentions": [{"type": "club", "id": 123, "screen_name": "club123", "text": "@club123"}, 
                         {"type": "id", "id": 1234, "screen_name": "id1234", "text": "@id1234"}],
            "have_reply": True
        }
    ]

class MockVkMethods:

    def __init__(self):
        pass
    
    class messages():
        async def getConversationMembers(peer_id):
            return {
                "response": {
                    "items": [
                        {
                            "member_id": 1234
                        },
                        {
                            "member_id": -123,
                            "is_admin": True
                        }
                    ]
                }
            }
        
@pytest.fixture()
def logical_rules_list():
    rules_list: list[BaseRule] = [
        TrueRule(),
        ~TrueRule(),
        TrueRule() & TrueRule(),
        TrueRule() & ~TrueRule(),
        ~TrueRule() & ~TrueRule(),
        TrueRule() | TrueRule(),
        TrueRule() | ~TrueRule(),
        ~TrueRule() & ~TrueRule(),
        TrueRule() | (~TrueRule() & ~TrueRule()),
        ~(~TrueRule() & ~TrueRule()),
        ContainsRule(triggers=["darky"]),
        ~ContainsRule(triggers=["darky"]),
        ContainsRule(triggers=["darky"]) | ~TrueRule(),
        ContainsRule(triggers=["darky"]) & ~TrueRule(),
        ContainsRule(triggers=["darky"]) & TrueRule(),
        ContainsRule(triggers=["darky"]) & TwiMLRule(value=["hello world <text>"])
    ]
    all_rules = []
    for rule in rules_list:
        rule.methods = MockVkMethods()
        all_rules.append(rule)
    return all_rules
        
@pytest.fixture()
def rules_list():
    rules_lst: list[BaseRule] = [
        TrueRule(),
        FalseRule(),
        ContainsRule(triggers=["test", "darky"], ignore_case=True),
        TextRule(value=["test", "test darky"], ignore_case=True),
        TwiMLRule(value=["test <variable>"], ignore_case=True),
        MentionRule(),
        IsMentionedRule(),
        ReplyRule(),
        ForwardRule(),
        AdminRule(),
        IsAdminRule(),
        InvitedRule(),
        IsInvitedRule()
    ]
    all_rules = []
    for rule in rules_lst:
        rule.methods = MockVkMethods()
        all_rules.append(rule)
    return all_rules

@pytest.fixture()
def fake_payload_event():
    return {
        "group_id": 123,
        "type": "message_event",
        "object": {
            "peer_id": 2000000001,
            "conversation_message_id": 1,
            "user_id": 1234
        }
    }

@pytest.fixture()
def payload_results():
    return [
        [False, False, False],
        [False, False, False],
        [False, True, False],
        [False, True, False],
        [True, True, False],
        [False, True, True]
    ]

@pytest.fixture()
def payload_rule_list():
    rules_lst: list[BaseRule] = [
        OnPayloadRule(payload={"test": "test"}),
        OnPayloadRule(),
        OnPayloadRule(payload={"test": "payload"})
    ]
    all_rules = []
    for rule in rules_lst:
        rule.methods = MockVkMethods()
        all_rules.append(rule)
    return all_rules