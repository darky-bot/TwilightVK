class DarkyError(Exception):
    def __init__(self, message:str=None):
        self.message=message
    
    def __str__(self):
        return f"{self.message}"
    
class InitError(DarkyError):
    pass


class VKAPIError(Exception):
    def __init__(self,
                 message:str=None,
                 method:str=None,
                 values:dict=None,
                 response:dict=None):
        self.message = message
        self.method = method
        self.values = values
        self.response = response
    
    def __str__(self):
        return f"{self.message}"
