import functools
import time


def omittable_bracket(f):
    """Decorator of decorator allowing decorator to be used as
     @decorator
     @decorator()

     Above 2 examples are equivalent.

     @decorator(args)
     """
    def deco_func(*args, **kwargs):
        if len(args) == 1 and not kwargs and callable(args[0]):
            # @decorator
            return f()(args[0])
        else:
            # @decorator(), or @decorator(arg1, kw=2)
            return f(*args, **kwargs)
    return deco_func


@omittable_bracket
def measure_time(count=10000):
    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal count
            start = time.perf_counter()
            print(f"{f.__name__} {count} trials:")
            result = None
            for _ in range(count):
                result = f(*args, **kwargs)
            process_time = time.perf_counter() - start
            print(f"It took {process_time} seconds.")
            return result
        return wrapper
    return deco
