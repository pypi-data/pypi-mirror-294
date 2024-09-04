import errno
import os
import platform
import signal
from functools import wraps


class TimeoutError(Exception):
    print("######################################## TIME OUT! ########################################")
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            strOS = platform.system()
            if strOS == "Linux":
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                if strOS == "Linux":
                    signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
