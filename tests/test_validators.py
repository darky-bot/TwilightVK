import json

import pytest
import pytest_asyncio

from twilight_vk.framework.validators import (
    HttpValidator,
    EventValidator,
    RequestValidator,
    ResponseValidator
)
from twilight_vk.framework.exceptions import(
    HttpValidationError,
    EventValidationError,
    ValidationError,
    VkApiError,
    LongPollError
)
from twilight_vk.utils.types.response import Response
from tests.fixtures.validators import (
    MockedHttpResponse,
    MockEvent,
    http_responses,
    event_responses,
    event_responses_results,
    request_params,
    outputs
)

from twilight_vk.utils.keyboard import KeyboardMarkup
from twilight_vk.utils.keyboard import CallbackActionKeyboardButton

async def fake_type_validating(*args, **kwargs):
    return True

@pytest.mark.asyncio
async def test_http_validator(http_responses, monkeypatch):
    monkeypatch.setattr(HttpValidator, "_isValid", fake_type_validating)

    # HTTPStatus.OK
    assert await HttpValidator.validate(http_responses[0]) == http_responses[0]

    # HTTPStatus.TEMPORARY_REDIRECT
    assert await HttpValidator.validate(http_responses[1]) == http_responses[1]

    # HTTPStatus.BAD_REQUEST
    with pytest.raises(HttpValidationError, match="Response validation error: Status code is not success "):
        await HttpValidator.validate(http_responses[2])

@pytest.mark.asyncio
async def test_event_validator(event_responses, event_responses_results):

    # Valid response
    assert await EventValidator.validate(event_responses[0]) == event_responses_results[0]

    # Invalid header
    with pytest.raises(EventValidationError, match="Response validation error: Content is not JSON "):
        await EventValidator.validate(event_responses[1])

    # Invalid response
    with pytest.raises(EventValidationError, match="Response validation error: Response doesn't contain the required fields "):
        await EventValidator.validate(event_responses[2])
    
    # Response from polling
    assert await EventValidator.validate(event_responses[3], True) == event_responses_results[3]
    
    # Error while polling
    with pytest.raises(LongPollError):
        await EventValidator.validate(event_responses[4])
    
    # Error while requesting VK API
    with pytest.raises(VkApiError):
        await EventValidator.validate(event_responses[5])

@pytest.mark.asyncio
async def test_request_validator(request_params):
    assert await RequestValidator.validate(request_params) == {
        "peer_ids": "123,456",
        "extended": "false",
        "forward": "{\"is_reply\": true}",
        "message": "abc-test"
    }

@pytest.mark.asyncio
async def test_response_validator(outputs):

    # MESSAGE_NEW with string output
    assert (await ResponseValidator.validate(outputs[0][1], 
                                             outputs[0][0])).getData() == Response(peer_ids=123,
                                                                                   message="Test output",
                                                                                   forward={"peer_id": 123,
                                                                                            "conversation_message_ids": 1,
                                                                                            "is_reply": True}).getData()
    
    # MESSAGE_NEW with string and keyboard tuple output
    assert (await ResponseValidator.validate(outputs[1][1], 
                                             outputs[1][0])).getData() == Response(peer_ids=123,
                                                                                   message="Test",
                                                                                   forward={"peer_id": 123,
                                                                                            "conversation_message_ids": 1,
                                                                                            "is_reply": True},
                                                                                   keyboard=KeyboardMarkup(inline=True, buttons=[[CallbackActionKeyboardButton(label="Test")]]).getMarkup()).getData()

    # MESSAGE_NEW with Response() output
    assert (await ResponseValidator.validate(outputs[2][1], 
                                             outputs[2][0])).getData() == Response(peer_ids=[123], 
                                                                                   message="Test output").getData()

    # LIKE_ADD with string output
    with pytest.raises(ValidationError, match=r"Validation error : Invalid response body"):
        await ResponseValidator.validate(outputs[3][1], 
                                         outputs[3][0])
        
    # LIKE_ADD with string and keyboard tuple output
    with pytest.raises(ValidationError, match=r"Validation error : Invalid response body"):
        await ResponseValidator.validate(outputs[4][1], 
                                         outputs[4][0])

    # LIKE_ADD with Response() output
    assert (await ResponseValidator.validate(outputs[5][1], 
                                             outputs[5][0])).getData() == Response(peer_ids=[123], 
                                                                                   message="Test output").getData()
    
    # MESSAGE_EVENT with string output
    assert (await ResponseValidator.validate(outputs[6][1], 
                                             outputs[6][0])).getData() == Response(peer_ids=123,
                                                                                   message="Test output",
                                                                                   forward={"peer_id": 123,
                                                                                            "conversation_message_ids": 1,
                                                                                            "is_reply": True}).getData()
    
    # MESSAGE_EVENT with string and keyboard tuple output
    assert (await ResponseValidator.validate(outputs[7][1], 
                                             outputs[7][0])).getData() == Response(peer_ids=123,
                                                                                   message="Test",
                                                                                   forward={"peer_id": 123,
                                                                                            "conversation_message_ids": 1,
                                                                                            "is_reply": True},
                                                                                   keyboard=KeyboardMarkup(inline=True, buttons=[[CallbackActionKeyboardButton(label="Test")]]).getMarkup()).getData()

    # MESSAGE_EVENT with Response() output
    assert (await ResponseValidator.validate(outputs[8][1], 
                                             outputs[8][0])).getData() == Response(peer_ids=[123], 
                                                                                   message="Test output").getData()