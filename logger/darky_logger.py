import logging.config, logging


class DarkyLogger:
    def __init__(self, logger_name:str="DARKYVK", configuration:dict=None) -> None:

        '''
        Класс DarkyLogger позволяет удобно инициализировать работу логгера logging, но с некоторыми модификациями

        :param logger_name:
        :type logger_name: str - используется для присвоения уникального имени логгеру
        (видно при использовании в форматировании %(name) или в файле логов при использовании встроенного formatters.DarkyFileFormatter)
        
        :param configuration:
        :type configuration: dict - позволяет гибко настроить конфигурацию логгера
        (см. https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema)
        По умолчанию берет конфигурацию из фреймворка DarkyVK
        '''

        if configuration is None:
            from utils.tools import Configuration
            configuration = Configuration().config["LOGGER"]

        logging.config.dictConfig(configuration)
        self.__logger__ = logging.getLogger(logger_name)
        self.__logger__.debug(f"DarkyLogger initiated")
    
    def __getattr__(self, name):

        if name not in ["debug", "info", "warning", "error", "critical"]:
            self.__logger__.warning(f"'DarkyLogger' has no attribute '{name}'. \"INFO\" is used instead.")
            name = "info"
        attr = getattr(self.__logger__, name)
        return attr
    
    def get_logger(self) -> logging.Logger:

        '''
        Клонирует уже созданный ранее логгер для его использования в других модулях
        '''

        self.__logger__.debug(f"'DarkyLogger.get_logger()' has been called")
        return self.__logger__