class DarkyAPIError(Exception):
    def __init__(self, message:str=None):
        self.message=message
    
    def __str__(self):
        return f"{self.message}"
    

class AuthError(DarkyAPIError):
    pass