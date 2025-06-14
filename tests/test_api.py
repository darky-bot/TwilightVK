import pytest
import asyncio

from darky_vk.http import async_http
from darky_vk import DarkyVK, DarkyAPI
from darky_vk.handlers.exceptions import AuthError

http = async_http.Http()

@pytest.mark.asyncio
async def test_init_failed():
    with pytest.raises(AuthError, match="ACCESS_TOKEN is None!"):
        DarkyAPI(FRAMEWORK=DarkyVK()).start()

@pytest.mark.asyncio
async def test_init_failed_accesstoken():
    with pytest.raises(AuthError, match="ACCESS_TOKEN is None!"):
        DarkyAPI(FRAMEWORK=DarkyVK(group_id=123)).start()

@pytest.mark.asyncio
async def test_init_failed_groupid():
    with pytest.raises(AuthError, match="GROUP_ID is None!"):
        DarkyAPI(FRAMEWORK=DarkyVK(access_token="123")).start()