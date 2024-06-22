
from functools import wraps
import inspect

def optional_debug(func):
    if 'debug' in inspect.getfullargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    # fix the signature of the function with added arguments
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    params.append(inspect.Parameter('debug',
                                   inspect.Parameter.KEYWORD_ONLY,
                                   default=False))
    wrapper.__signature__ = sig.replace(parameters=params)
    return wrapper


@optional_debug
def spam(a, b, c):
    print(a, b, c)



spam(1, 2, 3, debug=True)

print(inspect.signature(spam))

@optional_debug
def spam2(debug, a, b, c):
    print(a, b, c, debug)

