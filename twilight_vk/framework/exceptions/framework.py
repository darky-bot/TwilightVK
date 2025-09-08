class FrameworkError(Exception):
    
    def __init__(self,
                 message:str|None=None):
        '''
        Любые ошибки фреймворка

        :param message: Сообщение передаваемое вместе с исключением
        :type message: str | None
        '''
        self.message=message

    def __str__(self):
        return f"Framework got an error! {f"[{self.message}]" if self.message is not None else ""}"
    
class InitializationError(FrameworkError):
    
    def __init__(self,
                 access_token:str,
                 group_id:int):
        '''
        Ошибка инициализации класса TwilightVK

        :param access_token: Токен сообщества для авторизации
        :type access_token: str

        :param group_id: Идентификатор сообщества
        :type access_token: int
        '''
        self.__accessToken__ = access_token
        self.__groupId__ = group_id
    
    def __str__(self):
        return f"One of the requirement parameters is None! " \
        f"{": ACCESS_TOKEN is None) " if self.__accessToken__ is None else ""}"\
        f"{": GROUP_ID is None " if self.__groupId__ is None else ""}"