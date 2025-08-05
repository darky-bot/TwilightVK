class BaseRule:

    def __init__(self):
        self.event = None

    async def __updateEvent__(self, event):
        self.event = event
    
    async def check(self):
        pass


class TextRule(BaseRule):

    async def check(self, value:str|list[str], ignore_case:bool=True):
        text:str = self.event["object"]["message"]["text"]
        return (text.lower() if ignore_case else text) in ([val.lower() if ignore_case else value for val in value])


class Rules:
    list = {
        "BaseRule": BaseRule(),
        "TextRule": TextRule()
    }