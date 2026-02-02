import pytest
import asyncio
import pytest_asyncio
import pytest_httpbin
import pytest_mock

import twilight_vk

class MockedHttpGet:

    def __init__(self):
        self.response = {"response": {"result": "ok"}}
        self.url = "https://api.example.com/"
        self.method = "mocked-method"
        self.status = 200
        self.headers = {'Content-Type': 'application/json'}
    
    async def json(self):
        return self.response
    
    async def get(self, *args, **kwargs):
        return self

async def fake_get_method(*args, **kwargs):
   _response = MockedHttpGet()
   return await _response.json()

@pytest.mark.asyncio
async def test_methods(monkeypatch, mocker):

    _client = twilight_vk.TwilightVK(ACCESS_TOKEN="123", loop_wrapper=asyncio.get_event_loop_policy())

    http_validate_mock = mocker.AsyncMock()
    http_validate_mock.side_effect = lambda response, *args, **kwargs: response
    mocker.patch('twilight_vk.framework.methods.base.HttpValidator.validate', http_validate_mock)

    monkeypatch.setattr(_client.__bot__.base_methods.httpClient, "get", MockedHttpGet().get)

    assert await _client.methods.messages.send() == {"response": {"result": "ok"}}
    assert await _client.methods.users.get(user_ids=1) == {"response": {"result": "ok"}}
    assert await _client.methods.groups.getById() == {"response": {"result": "ok"}}