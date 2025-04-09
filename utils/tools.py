import yaml

class Configuration:

    def __init__(self, path:str="config.yaml"):
        self.config = None
        self.__path__ = path
        self.__load__()
    
    def __load__(self):
        with open(self.__path__, "r") as file:
            self.config = yaml.safe_load(file)
    
    def reload(self):
        self.__load__()