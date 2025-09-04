import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.methods import VkMethods

class ResponseHandler:

    def __init__(self,
                 peer_ids:int|list[int],
                 message:str|None=None,
                 attachments:str|list[str]=[],
                 reply_to:int|None=None,
                 forward:dict|None=None):
        '''
        Allows to send responses for the bot


        '''
        self.message = message
        self.peer_ids = peer_ids
        self.attachments = None
        self.reply_to = reply_to
        self.forward = json.dumps(forward) if forward is not None else None
    
    def getData(self) -> dict:
        '''
        Returns all data from initialized class
        '''
        return self.__dict__