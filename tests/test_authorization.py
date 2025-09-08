import pytest

import twilight_vk

class MockGetLongPollServer():

    def __init__(self, isSuccess=True):
        self.method = "GET"
        self.url = "https://fakeauth"
        self.headers = {"Content-Type": "application/json"}
        self.is_success = isSuccess

    async def json(self):
        if self.is_success:
            return {
                "response": {
                                "server": "https://fakeserverurl",
                                "key": "fakekey",
                                "ts": 0
                            }
            }
        return {
                    "error": {
                        "error_code": 5,
                        "error_msg": "User authorization failed: invalid access_token (4).",
                        "request_params": [
                            {
                                "key": "access_token",
                                "value": "123"
                            },
                            {
                                "key": "group_id",
                                "value": 123
                            },
                            {
                                "key": "v",
                                "value": "1.234"
                            }
                        ]
                    }
            }

@pytest.mark.asyncio
async def test_auth_failed(caplog, monkeypatch):
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123
    )

    async def fake_getBotLongPollServer():
        fake_response = MockGetLongPollServer(False)
        return await bot.__bot__.eventValidator.validate(fake_response)
    
    monkeypatch.setattr(bot.__bot__.vk_methods.groups, "getLongPollServer", fake_getBotLongPollServer)

    await bot.__bot__.auth()
    assert "Authrization error: [5] User authorization failed: invalid access_token (4)." in caplog.text

@pytest.mark.asyncio
async def test_auth_success(caplog, monkeypatch):
    bot = twilight_vk.TwilightVK(
        ACCESS_TOKEN="123",
        GROUP_ID=123
    )

    async def fake_getBotLongPollServer():
        fake_response = fake_response = MockGetLongPollServer(True)
        return await bot.__bot__.eventValidator.validate(fake_response)
    
    monkeypatch.setattr(bot.__bot__.vk_methods.groups, "getLongPollServer", fake_getBotLongPollServer)

    await bot.__bot__.auth()
    assert "Authorized" in caplog.text