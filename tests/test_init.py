import pytest
import asyncio
from fastapi.testclient import TestClient

from twilight_vk import DarkyVK, DarkyAPI
from twilight_vk.handlers.exceptions import AuthError

@pytest.mark.asyncio
async def test_with_no_parameters():
    with pytest.raises(AuthError, match="ACCESS_TOKEN is None!"):
        DarkyAPI(FRAMEWORK=DarkyVK()).start()

@pytest.mark.asyncio
async def test_with_no_access_idtoken():
    with pytest.raises(AuthError, match="ACCESS_TOKEN is None!"):
        DarkyAPI(FRAMEWORK=DarkyVK(GROUP_ID=123)).start()

@pytest.mark.asyncio
async def test_with_no_group_id():
    with pytest.raises(AuthError, match="GROUP_ID is None!"):
        DarkyAPI(FRAMEWORK=DarkyVK(ACCESS_TOKEN="123")).start()

@pytest.mark.asyncio
async def test_success_and_ping():
    client = TestClient(await DarkyAPI(FRAMEWORK=DarkyVK("123", 123)).get_api())
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"response": "pong"}