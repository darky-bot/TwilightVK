import yaml
from types import SimpleNamespace
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Configuration:

    def __init__(self, path:str|Path=BASE_DIR / "config.yaml"):

        '''
        Configuration initializing

        :param path: Path to the yaml configuration file
        :type path: str | Path
        '''
        self.__path__ = path
        self.config = SimpleNamespace()
        self._load_config()

    def _load_config(self):

        '''
        Loads the YAML configuration file and converts it to the object

        :param path: Path to the yaml configuration file
        :type path: str
        '''
        try:
            with open(self.__path__, "r", encoding="utf-8") as file:
                config_dict = yaml.safe_load(file)
                self._dict_to_object(config_dict)

        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.__path__}")
        
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error while parsing YAML file: {e}")
    
    def _dict_to_object(self, config_dict:dict):

        '''
        Converts dict to the object

        :param config_dict: Configuration dictionary you'd get in the _load_config()
        :type config_dict: dict
        '''
        if config_dict is None:
            raise ValueError("Configuration file is empty or invalid!")

        if not isinstance(config_dict, dict):
            raise TypeError(f"config_dict should be a dictionary!")

        self._dict_to_nested_object(config_dict, self.config)
    
    def _dict_to_nested_object(self, config_dict:dict, obj:object) -> None:
        
        for key, value in config_dict.items():
            if isinstance(value, dict):
                if key.startswith("JSON_"):
                    setattr(obj, key.lstrip("JSON_"), value)
                else:
                    nested_obj = SimpleNamespace()
                    setattr(obj, key, nested_obj)
                    self._dict_to_nested_object(value, nested_obj)
            else:
                setattr(obj, key, value)
        
    def reload(self, path:str=None):

        '''Updates the loaded configuration'''

        if path != None:
            self.__path__ = path

        self.config = SimpleNamespace()
        self._load_config()

    def get_config(self) -> object:

        '''Returns the loaded configuration'''

        return self.config