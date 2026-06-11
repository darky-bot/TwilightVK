from twilight_vk.logger.formatters import (
    DarkyConsoleFormatter,
    DarkyFileFormatter
)

CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "file": {
            "()": DarkyFileFormatter,
            "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
        },
        "console": {
            "()": DarkyConsoleFormatter,
            "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(message)s",
            "colored": True
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "tests/test_logging.log",
            "encoding": "utf8",
            "backupCount": 1
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console"
        }
    },
    "loggers": {
        "test": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}