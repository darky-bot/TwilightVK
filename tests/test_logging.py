import pytest
import asyncio
import logging

from twilight_vk.logger.darky_logger import DarkyLogger
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
            "filename": "test.log",
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
            "propagate": False
        }
    }
}

def test_logging():

    print()
    logger = DarkyLogger("test", CONFIG)

    for level in [logger.debug, logger.info, logger.warning, logger.error]:
        level(f"Mlem")
        level("{'key': 123}, {'access_token': 'abc'}, {\"access_token\": \"abc\"}")
        level(f"https://mlem.api/mlem?access_token=123")
        level(f"https://mlem.api/mlem?access_token=123&abs=True")
    logger.mlem("Mlem")
    try:
        raise Exception
    except Exception as ex:
        logger.critical(f"We got an error! Mlem", exc_info=True)