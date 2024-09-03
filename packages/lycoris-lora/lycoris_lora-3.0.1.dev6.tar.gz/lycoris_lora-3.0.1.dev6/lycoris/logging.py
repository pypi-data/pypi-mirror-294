import sys
import copy
import logging
from functools import cache


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",  # CYAN
        "INFO": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # YELLOW
        "ERROR": "\033[0;31m",  # RED
        "CRITICAL": "\033[0;37;41m",  # WHITE ON RED
        "RESET": "\033[0m",  # RESET COLOR
    }

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = self.COLORS.get(levelname, self.COLORS["RESET"])
        colored_record.levelname = f"{seq}{levelname}{self.COLORS['RESET']}"
        return super().format(colored_record)


logger = logging.getLogger("LyCORIS")
logger.propagate = False
logger.setLevel(logging.INFO)


if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColoredFormatter(
            "%(asctime)s|[%(name)s]-%(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(handler)


@cache
def info_once(msg):
    logger.info(msg)


@cache
def warning_once(msg):
    logger.warning(msg)


@cache
def error_once(msg):
    logger.error(msg)
