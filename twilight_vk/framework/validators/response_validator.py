from typing import TYPE_CHECKING
import logging

from ...utils.types.event_types import BotEventType
from ...utils.types.response import Response

logger = logging.getLogger("resp-validator")

class ResponseValidator:

    async def validate(response: 'Response | str',
                       event: dict = None):
        '''
        Response validator for custom handlers function's output

        :param response: Function's output
        :type response: str | Response

        :param event: Event object
        :type event: dict
        '''

        _event_type = event.get("type")
        _response_body = response

        logger.debug(f"Validating response for event {_event_type} with type {type(_response_body)}...")

        if _event_type in [
            BotEventType.MESSAGE_NEW,
            BotEventType.MESSAGE_REPLY,
            BotEventType.MESSAGE_EDIT,
            BotEventType.MESSAGE_TYPING_STATE,
            BotEventType.MESSAGE_READ,
            BotEventType.MESSAGE_EVENT
        ]:
            if isinstance(response, str):
                logger.debug(f"Got <string> output, converting to the <Response>...")
                _response_body = Response(
                    peer_ids=event["object"]["message"]["peer_id"],
                    message=f"{response}",
                    forward={
                        "peer_id": event["object"]["message"]["peer_id"],
                        "conversation_message_ids": event["object"]["message"]["conversation_message_id"],
                        "is_reply": True
                    }
                )
        
        logger.debug(f"Response body has been validated")
        
        return _response_body
