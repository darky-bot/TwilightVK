from ..logger.formatters import (
    DarkyConsoleFormatter,
    DarkyFileFormatter
)

class CONFIG:

    class FRAMEWORK:
        version = "0.1.0-beta"
        developer = "darky_wings"
    
    class VK_API:
        url = "https://api.vk.ru"
        version = "5.199"
        wait = 25

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
                },
                "handlers": {
                    "file": {
                        "level": "INIT",
                        "class": "logging.handlers.RotatingFileHandler",
                        "formatter": "file",
                        "filename": "twilight_vk.log",
                        "backupCount": 3,
                        "encoding": "utf-8"
                    },
                    "console": {
                        "level": "INIT",
                        "class": "logging.StreamHandler",
                        "formatter": "console"
                    }
                },
                "loggers": {
                    "twi-api-fw": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "twilight-vk": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "botslongpoll": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "vk-methods": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "http-validator": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "event-validator": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "event-handler": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    },
                    "rule-handler": {
                        "handlers": ["console", "file"],
                        "level": "INIT",
                        "propagate": True
                    }
                }
            }