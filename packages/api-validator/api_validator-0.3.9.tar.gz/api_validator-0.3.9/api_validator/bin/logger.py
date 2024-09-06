from loguru import logger
import sys
from os import environ


# taken from Loguru but with the addition of the extra field
def env(key, type_, default=None):
    if key not in environ:
        return default

    val = environ[key]

    if type_ == str:
        return val
    if type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    if type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None
    raise ValueError("The requested type '%r' is not supported" % type_)


LOG_FORMAT = env(
    "LOGURU_FORMAT",
    str,
    # "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "{message}",
    # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)


def init_logger():
    # Remove existing handlers
    logger.remove()
    stdout_handler = {
        "sink": sys.stdout,
        "serialize": False,
        "level": "INFO",
        "format": LOG_FORMAT,
    }
    logger.add(**stdout_handler)
    # logger.add(sys.stdout, format="{time} | {level} | {message}", filter="sub.module")
