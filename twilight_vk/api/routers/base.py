from fastapi import APIRouter

class BaseRouter:

    def __init__(self,
                 **kwargs):
        '''
        BaseRouter for API Swagger
        '''
        self.kwargs = kwargs
        self.__parseKwargs__()
        self.router = APIRouter()
    
    def __parseKwargs__(self):
        '''
        Parsing kwargs attribute, allowing to use each item as separate rule's attribute
        '''
        for key, value in self.kwargs.items():
            setattr(self, key, value)
    
    def get_router(self):
        return self.router