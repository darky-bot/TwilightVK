class ResponseValidator:

    def is_valid(self,
                 response:str):
        if type(response) != str:
            return False
        return True
    
class ResponseJSONValidator:

    def validate(self,
                 response:dict):
        if not ResponseValidator.validate(response):
            ...