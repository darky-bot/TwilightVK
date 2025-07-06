class DarkyError(Exception):
    pass
    
class InitError(DarkyError):
    pass

class ValidationError(DarkyError):
    pass



class VkApiError(DarkyError):
    pass

class AuthError(VkApiError):
    pass


class HttpError(DarkyError):
    pass

class IsNotSuccessCode(HttpError):
    pass