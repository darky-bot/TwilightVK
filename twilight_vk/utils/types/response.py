import json

class Response:

    def __init__(self,
                 peer_ids: int | list[int] = None,
                 domain: str = None,
                 chat_id: int = None,
                 message: str = None,
                 lat: str = None,
                 long: str = None,
                 attachment: str | list[str] = None,
                 reply_to: int = None,
                 forward_messages: int | list[int] = None,
                 forward: dict = None,
                 sticker_id: int = None,
                 keyboard: object = None,
                 template: object = None,
                 payload: object = None,
                 content_source: dict = None,
                 dont_parse_links: bool = None,
                 disable_mentions: bool = None):
        '''
        Allows to convert str to OutputHandler
        '''
        self.peer_ids = peer_ids
        self.domain = domain
        self.chat_id = chat_id
        self.message = message

        self.lat = lat
        self.long = long

        self.attachment = attachment

        self.reply_to = reply_to
        self.forward_messages = forward_messages
        self.forward = forward

        self.sticker_id = sticker_id
        
        self.keyboard = keyboard
        self.template = template
        self.payload = payload
        self.content_source = content_source
        self.dont_parse_links = dont_parse_links
        self.disable_mentions = disable_mentions
    
    def getData(self) -> dict:
        '''
        Returns all data from initialized class
        '''
        return self.__dict__