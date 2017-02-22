from functools import wraps
from contextlib import contextmanager
import time
import inspect

_DEBUG = False


@contextmanager
def Timer(name, debug=_DEBUG):
    if not debug:
        yield
        return
    try:
        start = time.time()
        yield
    except Exception as e:
        raise e
    finally:
        end = time.time()

        path = [name]
        for frame in inspect.stack()[2:]:
            if frame[3] == "<module>":
                break
            path.append(frame[3])

        path_str = ".".join(reversed(path))
        print("Timer: {}: {:0.5f}s".format(path_str, end-start))


def timer(fxn):
    @wraps(fxn)
    def _(*args, **kwargs):
        with Timer(fxn.__name__ + '()'):
            return fxn(*args, **kwargs)
    return _
