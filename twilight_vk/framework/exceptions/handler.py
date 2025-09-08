from ..handlers.response import ResponseHandler
from .framework import FrameworkError

class HandlerError(FrameworkError):

    def __init__(self,
                 message:str):
        '''
        Базовое исключение обработчика

        :param message: Опционально. Дополнительная информация об ошибке
        :type message: str
        '''
        self.message = message
    
    def __str__(self):
        return f"Handler error"\
        f"{f" : {self.message}" if self.message is not None else ""}"
    

class ResponseHandlerError(HandlerError):

    def __init__(self,
                 callback):
        '''
        Исключение обработчика ответов

        :param callback: Ответ от функции, которая выполнилась в обработчике событий
        '''
        self.callback = callback
    
    def __str__(self):
        return f"Response handler error"\
        f"{f" : function callback is not instance of ResponseHandler, make sure you are returning correct values in your functions"\
           if not isinstance(self.callback, ResponseHandler) else ""}"