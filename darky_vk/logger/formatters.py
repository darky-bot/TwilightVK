import re
import logging

from ..utils.darky_visual import STYLE, FG, BG


class DarkyConsoleFormatter(logging.Formatter):

    def format(self, record):

        match record.levelname:
            case "DEBUG": record.levelname =    f"{FG.BLUE}{record.levelname}{STYLE.RESET}"
            case "INFO": record.levelname =     f"{FG.GREEN}{record.levelname}{STYLE.RESET}"
            case "WARNING": record.levelname =  f"{FG.YELLOW}{STYLE.RESET}"
            case "ERROR": 
                record.levelname =              f"{STYLE.BOLD}{FG.RED}{record.levelname}{STYLE.RESET}"
            case "CRITICAL": 
                record.levelname =              f"{STYLE.BOLD}{BG.RED}{FG.WHITE}{record.levelname}{STYLE.RESET}"
                record.msg =                    f"{FG.RED}{record.msg}{STYLE.RESET}"

        return super().format(record)
    
    def formatException(self, ei):
        return f"{FG.RED}{super().formatException(ei)}{STYLE.RESET}"

class DarkyFileFormatter(logging.Formatter):

    def format(self, record):
        record.asctime =        re.sub(r'\033\[.*?m', '', record.asctime)
        record.levelname =      re.sub(r'\033\[.*?m', '', record.levelname)
        record.msg =            re.sub(r'\033\[.*?m', '', record.msg)
        if record.exc_text is not None:
            record.exc_text =   re.sub(r'\033\[.*?m', '', record.exc_text)

        return super().format(record)
