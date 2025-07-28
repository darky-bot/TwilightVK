from aiohttp import ClientResponse

class FrameworkError(Exception):
    pass
    
class InitError(FrameworkError):
    pass

class HttpValidationError(FrameworkError):
    
    def __init__(self,
                 isValid:bool,
                 isSuccess:bool,
                 response:ClientResponse):
        self.isRaw = isValid
        self.isSuccess = isSuccess
        self.response = response



class VkApiError(FrameworkError):
    pass

class AuthError(VkApiError):
    pass