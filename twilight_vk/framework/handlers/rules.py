class BaseRule:

    def __init__(self, **kwargs):
        self.event = None
        self.kwargs = kwargs

    async def __updateEvent__(self, event):
        self.event = event
    
    async def check(self) -> bool:
        pass


class TextRule(BaseRule):

    '''
    Сверяет текст сообщения с указанным, возвращает True при совпадении

    :param value: Ожидаемое значение
    :type value: str | list[str]

    :param ignore_case: Флаг игнорирования регистра
    :type ignore_case: bool
    '''

    async def check(self) -> bool:
        text:str = self.event["object"]["message"]["text"]
        return (text.lower() if self.kwargs["ignore_case"] else text) in \
            ([val.lower() if self.kwargs["ignore_case"] else self.kwargs["value"] for val in self.kwargs["value"]])