import pytest
import pytest_asyncio

from twilight_vk.framework.handlers.event_handlers import DEFAULT_HANDLER
from tests.fixtures.rules import (
    BaseRule,
    fake_event,
    messages_list,
    results,
    handler_results,
    rules_list,
    MockVkMethods
)

@pytest.mark.asyncio
async def test_rules(fake_event: dict, messages_list: list, results: list, rules_list: list[BaseRule]):
    for test in range(len(messages_list["messages"])):
        fake_event["object"]["message"]["text"] = messages_list["messages"][test]
        fake_event["object"]["message"]["reply_message"] = messages_list["replies"][test]
        if fake_event["object"]["message"]["reply_message"] == None:
            fake_event["object"]["message"].__delitem__("reply_message")
        fake_event["object"]["message"]["fwd_messages"] = messages_list["fwds"][test]
        fake_event["object"]["message"]["action"] = messages_list["actions"][test]
        if fake_event["object"]["message"]["action"] == None:
            fake_event["object"]["message"].__delitem__("action")
        rule_results = [await rule._check(fake_event) for rule in rules_list]
        assert rule_results == results[test]

@pytest.mark.asyncio
async def test_handlerinput(fake_event: dict, messages_list: list, results: list, rules_list: list[BaseRule], handler_results: list):
    for test in range(len(messages_list["messages"])):
        fake_event["object"]["message"]["text"] = messages_list["messages"][test]
        rule_results = [await rule._check(fake_event) for rule in rules_list]
        handler_result = await DEFAULT_HANDLER(MockVkMethods())._extractArgs(rule_results)
        assert handler_result == handler_results[test]