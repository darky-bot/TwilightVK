import pytest, pytest_asyncio
import dotenv, os
import re
import asyncio
import logging

import twilight_vk
from twilight_vk.framework.handlers.exceptions import (
    AuthError,
    TwilightInitError
)

dotenv.load_dotenv()

@pytest.mark.asyncio
async def test_framework_invalid_initialization():
    with pytest.raises(TwilightInitError):
        twilight_vk.TwilightVK()

@pytest.mark.asyncio
async def test_botlongpoll_auth_func_failed(caplog):
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123
    )
    await bot.__bot__.auth()
    assert "Authrization error: [5] User authorization failed: invalid access_token (4)." in caplog.text

@pytest.fixture
async def get_authorized_bot():
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN=os.getenv("ACCESS_TOKEN"),
        GROUP_ID=os.getenv("GROUP_ID")
    )
    await bot.__bot__.auth()
    return bot

@pytest.mark.asyncio
async def test_botlongpoll_auth_func_success(caplog):
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN=os.getenv("ACCESS_TOKEN"),
        GROUP_ID=os.getenv("GROUP_ID")
    )
    await bot.__bot__.auth()
    assert "Authorized" in caplog.text

@pytest.mark.asyncio
async def test_botlongpoll_check_event_func():
    bot: twilight_vk.TwilightVK = get_authorized_bot()
    response = await bot.__bot__.check_event()
    assert response.keys() == {"ts": 0, "updates": []}.keys()

#TODO: event handler tests
#TODO: methods tests
#TODO: errors tests