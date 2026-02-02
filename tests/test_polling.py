import asyncio

import pytest
import pytest_asyncio
import pytest_mock

from twilight_vk import TwilightVK
from twilight_vk.utils.types.twi_states import TwiVKStates
from tests.fixtures.polling import (
    bot,
    MockEventGenerator
)

@pytest.mark.asyncio
async def test_authorization(bot: TwilightVK, caplog, monkeypatch, mocker):

    http_validate_mock = mocker.AsyncMock()
    http_validate_mock.side_effect = lambda response, *args, **kwargs: response
    mocker.patch('twilight_vk.framework.methods.base.HttpValidator.validate', http_validate_mock)

    monkeypatch.setattr(bot.__bot__.vk_methods.groups.base_api.httpClient, "get", MockEventGenerator("auth fail").get)
    await bot.__bot__.auth()
    assert bot.__bot__.__server__ is None
    assert bot.__bot__.__key__ is None
    assert bot.__bot__.__ts__ is None
    assert "Authrization error: [5] User authorization failed: invalid access_token (4)." in caplog.text

    monkeypatch.setattr(bot.__bot__.vk_methods.groups.base_api.httpClient, "get", MockEventGenerator("auth success").get)
    await bot.__bot__.auth()
    assert bot.__bot__.__server__ is not None
    assert bot.__bot__.__key__ is not None
    assert bot.__bot__.__ts__ is not None
    assert "Authorized" in caplog.text

@pytest.mark.asyncio
async def test_check_event(bot: TwilightVK, caplog, monkeypatch, mocker):
    
    http_validate_mock = mocker.AsyncMock()
    http_validate_mock.side_effect = lambda response, *args, **kwargs: response
    mocker.patch('twilight_vk.framework.polling.bots_longpoll.HttpValidator.validate', http_validate_mock)

    monkeypatch.setattr(bot.__bot__.httpClient, "get", MockEventGenerator("message_typing_state").get)
    assert await bot.__bot__.check_event() == await MockEventGenerator("message_typing_state").json()

@pytest.mark.asyncio
async def test_polling_listen(bot: TwilightVK, caplog, monkeypatch, mocker):
    
    http_validate_mock = mocker.AsyncMock()
    http_validate_mock.side_effect = lambda response, *args, **kwargs: response
    mocker.patch('twilight_vk.framework.polling.bots_longpoll.HttpValidator.validate', http_validate_mock)

    monkeypatch.setattr(bot.__bot__.httpClient, "get", MockEventGenerator("message_new").get)
    async for event in bot.__bot__.listen():
        assert event == await MockEventGenerator("message_new").json()
        break

@pytest.mark.asyncio
async def test_failed_polling(bot: TwilightVK, caplog, monkeypatch, mocker):
    
    http_validate_mock = mocker.AsyncMock()
    http_validate_mock.side_effect = lambda response, *args, **kwargs: response
    mocker.patch('twilight_vk.framework.polling.bots_longpoll.HttpValidator.validate', http_validate_mock)

    bot._state = TwiVKStates.READY

    bot.should_stop()

    monkeypatch.setattr(bot.__bot__.vk_methods.groups.base_api.httpClient, "get", MockEventGenerator("auth success").get)

    failed_codes = ["1", "2", "3"]

    for code in failed_codes:
        monkeypatch.setattr(bot.__bot__.httpClient, "get", MockEventGenerator(f"failed event {code}").get)
        await bot.__bot__.check_event()

        if code == "1":
            assert bot.__bot__.__ts__ == 321
    
    assert "The event history is outdated or has been partially lost. The application can receive events further using the new \"ts\" value from the response." in caplog.text
    assert "The key is expired. Getting new one..." in caplog.text
    assert "The information is lost. Reauthorizing..." in caplog.text

@pytest.mark.asyncio
async def test_graceful_stop_polling(bot: TwilightVK, caplog, monkeypatch):

    bot._state = TwiVKStates.READY
    
    bot.should_stop()
    assert "Polling will be stopped as soon as the current request will be done. Please wait" in caplog.text
    assert bot._state == TwiVKStates.SHUTTING_DOWN