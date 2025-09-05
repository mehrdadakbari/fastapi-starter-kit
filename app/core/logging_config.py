import sys
import logging
from logging.config import dictConfig
from pythonjsonlogger import jsonlogger

# --------------------
# Custom log level
# --------------------
SUCCESS_LEVEL_NUM = 25  # between INFO (20) and WARNING (30)
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

logging.Logger.success = success


# --------------------
# ANSI color codes
# --------------------
COLOR_CODES = {
    "DEBUG": "\033[36m",     # Cyan
    "INFO": "\033[37m",      # White
    "SUCCESS": "\033[32m",   # Green
    "WARNING": "\033[33m",   # Yellow
    "ERROR": "\033[31m",     # Red
    "CRITICAL": "\033[41m",  # Red background
}
RESET_CODE = "\033[0m"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = "%(levelname)s %(asctime)s [pid:%(process)d] [%(name)s:%(lineno)d] - %(message)s"
        date_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(log_fmt, date_fmt)
        formatted = formatter.format(record)
        color = COLOR_CODES.get(record.levelname, RESET_CODE)
        return f"{color}{formatted}{RESET_CODE}"


class JsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self):
        super().__init__(
            "%(levelname)s %(asctime)s %(process)d %(name)s %(lineno)d %(message)s"
        )


# --------------------
# Logging configs
# --------------------
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {"()": ColorFormatter},
        "json": {"()": JsonFormatter},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": sys.stdout,
        },
        "json_console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "fastapi": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "__main__": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}


# --------------------
# Setup function
# --------------------
def setup_logging(env: str = "dev"):
    """
    Setup logging configuration.
    - env="dev" -> colored logs
    - env="prod" -> json logs
    """
    config = LOGGING_CONFIG.copy()

    if env == "prod":
        config["root"]["handlers"] = ["json_console"]
        for logger in config["loggers"].values():
            logger["handlers"] = ["json_console"]

    dictConfig(config)

    # Silence noisy libraries
    for name in logging.root.manager.loggerDict.keys():
        if name.startswith("pymongo"):
            logging.getLogger(name).setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
