from aiohttp import ClientResponse

class FrameworkError(Exception):
    
    def __init__(self,
                 message:str=None):
        self.message=message

    def __str__(self):
        return f"Framework got an error! {f"[{self.message}]" if self.message is not None else ""}"
    
class InitError(FrameworkError):
    
    def __init__(self,
                 access_token:str,
                 group_id:int):
        self.__accessToken__ = access_token
        self.__groupId__ = group_id
    
    def __str__(self):
        return f"One of the requirement parameters is None! " \
        f"{"(ACCESS_TOKEN is None) " if self.__accessToken__ is None else ""}"\
        f"{"(GROUP_ID is None) " if self.__groupId__ is None else ""}"

class HttpValidationError(FrameworkError):
    
    def __init__(self,
                 isValid:bool,
                 isSuccess:bool,
                 response:ClientResponse):
        self.isRaw = isValid
        self.isSuccess = isSuccess
        self.response = response
    
    def __str__(self):
        return f"Response validation error"\
        f"{": Is not valid raw " if self.isRaw is None else ""}"\
        f"{": Status code is not success " if self.isSuccess is None else ""}"

class EventValidationError(FrameworkError):

    def __init__(self,
                 jsonIsValid:bool,
                 fieldsAreValid:bool,
                 content:dict):
        self.jsonIsValid = jsonIsValid
        self.fieldsAreValid = fieldsAreValid
        self.content = content

    def __str__(self):
        return f"Response validation error"\
        f"{": Content is not JSON " if self.jsonIsValid is None else ""}"\
        f"{": Response doesn't contain the required fields " if self.fieldsAreValid is None else ""}"

class VkApiError(FrameworkError):
    
    def __init__(self,
                 error_code:int,
                 error_msg:str,
                 request_params:list,
                 ):
        self.error_code = error_code
        self.error_msg = error_msg
        self.request_params = request_params
    
    def __str__(self):
        return f"[{self.error_code}] {self.error_msg}"

class AuthError(VkApiError):
    pass