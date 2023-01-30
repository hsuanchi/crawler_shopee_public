import time
import logging

logger = logging.getLogger(__name__)


def timer(function):
    def wrapper(*args, **kws):
        t_start = time.time()
        result = function(*args, **kws)
        t_end = time.time()
        t_count = t_end - t_start
        logger.info(f"[{function.__qualname__}] - Time Coast: {t_count:.2f}s")
        return result

    return wrapper
