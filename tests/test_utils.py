import asyncio
from typing import Any

import pytest
import pytest_asyncio

from twilight_vk.utils.event_loop import TwiTaskManager
from twilight_vk.utils.twiml import TwiML
from tests.fixtures.utils import (
    loop,
    log_fixture,
    twiml,
    parse_dataset,
    mentions_dataset
)

async def fake_coro1(wrapper: TwiTaskManager):
    wrapper.logger.info("Hello")

async def fake_coro2(wrapper: TwiTaskManager):
    wrapper.logger.info("World")

async def fake_coro3(wrapper: TwiTaskManager):
    wrapper.logger.info("fake-coro3 start")
    await wrapper._handle_sigterm()
    await asyncio.sleep(5)
    wrapper.logger.info("fake-coro3 end")

async def fake_coro4(wrapper: TwiTaskManager):
    wrapper.logger.info("Test1")

async def fake_coro5(wrapper: TwiTaskManager):
    wrapper.logger.info("Test2")


def test_twi_task_manager(loop: TwiTaskManager,
                          log_fixture: Any):
    loop.add_task(fake_coro1(loop))
    loop.add_task(fake_coro2(loop))
    loop.run()
    assert "Hello" in log_fixture.text
    assert "World" in log_fixture.text

    loop.add_task(fake_coro3(loop))
    loop.run()
    assert "fake-coro3 start" in log_fixture.text
    assert "fake-coro3 end" not in log_fixture.text

    loop.add_task([fake_coro4(loop), fake_coro5(loop)])
    loop.run()
    assert "Test1" in log_fixture.text
    assert "Test2" in log_fixture.text

    loop.stop()
    assert "Stopping all tasks..." in log_fixture.text
    assert "Tasks was stopped" in log_fixture.text

@pytest.mark.asyncio
async def test_twiml_parse_params(twiml: TwiML,
                                  parse_dataset: dict):
    for _temp in range(len(parse_dataset.get("templates"))):
        twiml.update_template(parse_dataset.get("templates")[_temp])
        for _msg in range(len(parse_dataset.get("messages"))):
            result = await twiml.parse(parse_dataset.get("messages")[_msg])
            assert result == parse_dataset.get("results")[_temp][_msg]

@pytest.mark.asyncio
async def test_twiml_extract_mentions(twiml: TwiML,
                                      mentions_dataset: dict):
    for _msg in range(len(mentions_dataset.get("messages"))):
        mentions = await twiml.extract_mentions(mentions_dataset.get("messages")[_msg])
        assert mentions == mentions_dataset.get("results")[_msg]