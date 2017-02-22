from functools import wraps
from contextlib import contextmanager
import time


@contextmanager
def Timer(name):
    print("Starting task: " + name)
    start = time.time()
    try:
        yield
    except Exception as e:
        raise e
    finally:
        dt = time.time() - start
        print("Ended task: {}: {:0.4f}s".format(name, dt))


def timer(fxn):
    @wraps(fxn)
    def _(*args, **kwargs):
        with Timer(fxn.__name__ + '()'):
            return fxn(*args, **kwargs)
    return _
