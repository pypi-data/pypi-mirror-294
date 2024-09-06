import time
from . import log_utils


logger = log_utils.get_logger('debug')


def debug_timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.print(f"{func.__name__} took {time.time() - start:.2f} seconds")
        return result
    return wrapper
