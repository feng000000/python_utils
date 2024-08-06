from typing import Callable

def noexcept(func: Callable):
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return e

    return wraper
