from typing import TYPE_CHECKING
import logging

from ...framework.exceptions.validator import ValidationError
from ...utils.types.event_types import BotEventType
from ...utils.types.response import Response
from ...utils.keyboard import KeyboardMarkup

logger = logging.getLogger("resp-validator")

class ResponseValidator:

    @staticmethod
    def _convert(event: dict, message: str, keyboard_markup: KeyboardMarkup = None) -> 'Response':
        return Response(
            peer_ids = event["peer_id"],
            message = f"{message}",
            forward = {
                "peer_id": event["peer_id"],
                "conversation_message_ids": event.get("conversation_message_id", None),
                "is_reply": True
            },
            keyboard = keyboard_markup
        )

    async def validate(response: 'Response | str',
                       event: dict = None) -> Response:
        '''
        Response validator for custom handlers function's output

        :param response: Function's output
        :type response: str | Response

        :param event: Event object
        :type event: dict
        '''

        _event_type = event.get("type")
        _event_object = event
        _response_body = response

        logger.debug(f"Validating response for event {_event_type} with type {type(_response_body)}...")

        if isinstance(response, Response):
            return _response_body

        if _event_type in [
            BotEventType.MESSAGE_NEW,
            BotEventType.MESSAGE_EVENT
        ]:
            _event_object = event["object"]["message"] if _event_type == BotEventType.MESSAGE_NEW else event["object"]
        
            if isinstance(response, str):
                logger.debug(f"Got <string> output, converting to the <Response>...")
                _response_body = ResponseValidator._convert(_event_object, response)
            
            elif isinstance(response, tuple):
                logger.debug(f"Got <string, KeyboardMarkup> output, converting to the <Response>...")
                _response_body = ResponseValidator._convert(_event_object, response[0], response[1])

        if not isinstance(_response_body, Response):
            raise ValidationError(response = _response_body,
                                  message="Invalid response body")
        
        logger.debug(f"Response body has been validated")
        
        return _response_body
