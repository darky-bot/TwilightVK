import pytest
import pytest_asyncio

from twilight_vk.framework.handlers.event_handlers import DEFAULT_HANDLER
from tests.fixtures.rules import (
    BaseRule,
    fake_event,
    fake_payload_event,
    logic_rules_results,
    logical_rules_list,
    messages_list,
    results,
    non_message_new_results,
    handler_results,
    payload_results,
    payload_rule_list,
    rules_list,
    MockVkMethods
)

@pytest.mark.asyncio
async def test_logic_rules(fake_event: dict, logical_rules_list: list[BaseRule], logic_rules_results: list[bool]):
    fake_event["object"]["message"]["text"] = "hello world darky pony"
    for i in range(len(logical_rules_list)):
        rule_result = await logical_rules_list[i]._check(fake_event, MockVkMethods())
        assert rule_result == logic_rules_results[i]

@pytest.mark.asyncio
async def test_rules(fake_event: dict, messages_list: list, results: list, non_message_new_results: list, rules_list: list[BaseRule]):
    for test in range(len(messages_list["messages"])):
        fake_event["object"]["message"]["text"] = messages_list["messages"][test]
        fake_event["object"]["message"]["reply_message"] = messages_list["replies"][test]
        if fake_event["object"]["message"]["reply_message"] == None:
            fake_event["object"]["message"].__delitem__("reply_message")
        fake_event["object"]["message"]["fwd_messages"] = messages_list["fwds"][test]
        fake_event["object"]["message"]["action"] = messages_list["actions"][test]
        if fake_event["object"]["message"]["action"] == None:
            fake_event["object"]["message"].__delitem__("action")
        rule_results = [await rule._check(fake_event, MockVkMethods()) for rule in rules_list]
        assert rule_results == results[test]
    fake_event["type"] = "message_reply"
    rule_results = [await rule._check(fake_event, MockVkMethods()) for rule in rules_list]
    assert rule_results == non_message_new_results[0]

@pytest.mark.asyncio
async def test_handlerinput(fake_event: dict, messages_list: list, results: list, rules_list: list[BaseRule], handler_results: list):
    for test in range(len(messages_list["messages"])):
        fake_event["object"]["message"]["text"] = messages_list["messages"][test]
        fake_event["object"]["message"]["reply_message"] = messages_list["replies"][test]
        if fake_event["object"]["message"]["reply_message"] == None:
            fake_event["object"]["message"].__delitem__("reply_message")
        fake_event["object"]["message"]["fwd_messages"] = messages_list["fwds"][test]
        fake_event["object"]["message"]["action"] = messages_list["actions"][test]
        if fake_event["object"]["message"]["action"] == None:
            fake_event["object"]["message"].__delitem__("action")
        rule_results = [await rule._check(fake_event, MockVkMethods()) for rule in rules_list]
        handler_result = await DEFAULT_HANDLER(MockVkMethods())._extractArgs(rule_results)
        assert handler_result == handler_results[test]

@pytest.mark.asyncio
async def test_payloadrule(fake_payload_event: dict, messages_list: list, payload_results: list, payload_rule_list: list[BaseRule]):
    for test in range(len(messages_list["payloads"])):
        if "payload" in fake_payload_event["object"]:
            fake_payload_event["object"].__delitem__("payload")
        if messages_list["payloads"][test] is not None:
            fake_payload_event["object"]["payload"] = messages_list["payloads"][test]
        rule_results = [await rule._check(fake_payload_event, MockVkMethods()) for rule in payload_rule_list]
        assert rule_results == payload_results[test]