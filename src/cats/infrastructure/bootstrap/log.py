import logging
import sys

from pythonjsonlogger import jsonlogger


def setup_logger() -> None:
    format_ = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"
    formatter = jsonlogger.JsonFormatter(format_)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
