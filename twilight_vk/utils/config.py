from ..logger.formatters import (
    DarkyConsoleFormatter,
    DarkyFileFormatter,
    UvicornAccessFormatter
)

class CONFIG:

    class FRAMEWORK:
        version = "0.2.0-beta3"
        developer = "darky_wings"
    
    class VK_API:
        url = "https://api.vk.ru"
        version = "5.199"
        wait = 25

    class API:
        host = "0.0.0.0"
        port = 8000
        title = "Twilight API Swagger"
        description = "Welcome to the Twilight API Swagger!"
        version = "0.0.1"
        prefix = "/api/v1"

    LOGGER = {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "file": {
                        "()": DarkyFileFormatter,
                        "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
                    },
                    "console": {
                        "()": DarkyConsoleFormatter,
                        "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(message)s",
                        "colored": True,
                        "color_core_name": True
                    },
                    "uvicorn_access_console": {
                        "()": UvicornAccessFormatter,
                        "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(client_addr)s - \"%(request_line)s\" %(status_code)s",
                        "colored": True
                    }
                },
                "handlers": {
                    "file": {
                        "level": "DEBUG",
                        "class": "logging.handlers.RotatingFileHandler",
                        "formatter": "file",
                        "filename": "twilight_vk.log",
                        "backupCount": 3,
                        "encoding": "utf-8"
                    },
                    "console": {
                        "level": "INFO",
                        "class": "logging.StreamHandler",
                        "formatter": "console"
                    },
                    "uvicorn_access_console": {
                        "level": "DEBUG",
                        "class": "logging.StreamHandler",
                        "formatter": "uvicorn_access_console"
                    }
                },
                "loggers": {
                    "twilight-api": {
                        "handlers": ["console", "file"],
                        "level": "DEBUG",
                        "propagate": False
                    },
                    "uvicorn.access": {
                        "handlers": ["uvicorn_access_console", "file"],
                        "level": "DEBUG",
                        "propagate": False
                    },
                    "uvicorn.error": {
                        "handlers": ["uvicorn_access_console", "file"],
                        "level": "WARNING",
                        "propagate": False
                    },
                    "twilight-vk": {
                        "handlers": ["console", "file"],
                        "level": "DEBUG",
                        "propagate": False
                    }
                },
                "root": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"]
                }
            }