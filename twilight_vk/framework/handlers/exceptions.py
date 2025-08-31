from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..handlers.response import ResponseHandler

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
    
class TwilightInitError(FrameworkError):
    
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



class ValidationError(FrameworkError):
    
    def __init__(self,
                 response:dict|ClientResponse,
                 message:str|None=None):
        '''
        Базовый класс ошибки валидации

        :param response: Ответ HTTP запроса или тело ответа
        :type response: dict | ClientResponse
        '''
        self.response = response
        self.message = message
    
    def __str__(self):
        return f"Validation error"\
        f"{f" : {self.message}" if self.message is not None else ""}"

class HttpValidationError(ValidationError):
    
    def __init__(self,
                 isValid:bool,
                 isSuccess:bool,
                 response:ClientResponse):
        '''
        Ошибка валидации ответов от любых HTTP запросов
        Возникает при некорректном raw-формате ответа либо при кодах ответа которые не соответствуют успешным кодам

        :param isValid: Результат проверки RAW
        :type isValid: bool

        :param isSuccess: Результат проверки успешного кода в ответе
        :type isSuccess: bool

        :param response: Ответ от HTTP запроса
        :type response: ClientResponse
        '''
        self.isRaw = isValid
        self.isSuccess = isSuccess
        self.response = response
    
    def __str__(self):
        return f"Response validation error"\
        f"{": Is not valid raw " if self.isRaw is None else ""}"\
        f"{": Status code is not success " if self.isSuccess is None else ""}"

class EventValidationError(ValidationError):

    def __init__(self,
                 jsonIsValid:bool,
                 fieldsAreValid:bool,
                 content:dict):
        '''
        Ошибка валидации ответов от API
        Возникает при ошибках в ответе или при некорректном формате

        :param jsonIsValid: Результат проверки наличия JSON в теле ответа
        :type jsonIsValid: bool

        :param fieldsAreValid: Результат проверки обязательных полей в теле ответа
        :type fieldsAreValid: bool

        :param content: Тело ответа в формате JSON
        :type response: dict
        '''
        self.jsonIsValid = jsonIsValid
        self.fieldsAreValid = fieldsAreValid
        self.content = content

    def __str__(self):
        return f"Response validation error"\
        f"{": Content is not JSON " if self.jsonIsValid is None else ""}"\
        f"{": Response doesn't contain the required fields " if self.fieldsAreValid is None else ""}"



class HandlerError(FrameworkError):

    def __init__(self,
                 message:str):
        self.message = message
    
    def __str__(self):
        return f"Handler error"\
        f"{f" : {self.message}" if self.message is not None else ""}"
    

class ResponseHandlerError(HandlerError):

    def __init__(self,
                 callback):
        self.callback = callback
        self.instance:"ResponseHandler"
    
    def __str__(self):
        return f"Response handler error"\
        f"{f" : function callback is not instance of ResponseHandler, make sure you are returning correct values in your functions"\
           if not isinstance(self.callback, self.instance) else ""}"


class VkApiError(FrameworkError):
    
    def __init__(self,
                 error_code:int,
                 error_msg:str,
                 request_params:list,
                 ):
        '''
        Исключение при ошибках в запросах к VK API

        :param error_code: Код ошибки
        :type error_code: int

        :param error_msg: Сообщение ошибки
        :type error_msg: str

        :param request_params: Переданные с запросом HTTP параметры
        :type request_params: list
        '''
        self.error_code = error_code
        self.error_msg = error_msg
        self.request_params = request_params
    
    def __str__(self):
        return f"[{self.error_code}] {self.error_msg}"

class AuthError(VkApiError):
    '''Ошибка авторизации в API'''
    pass