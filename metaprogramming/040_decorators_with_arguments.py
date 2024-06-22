# @decorator(x, y, z)
# def func(a, b):
#   ...
#
# is equivalent to
#
# def func(a, b):
#   ...
#
# func = decorator(x, y, z)(func)
#
# the result of decorator(x, y, z) must be a callable which, in
# turn, takes a function as input and wraps it

import logging
from functools import wraps

def logged(level, name=None, message=None):
    '''
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    '''

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        return wrapper

    return decorate


logging.basicConfig(level=logging.DEBUG)


@logged(logging.CRITICAL)
def add(x, y):
    return x + y

@logged(logging.DEBUG, 'example')
def spam():
    print('Spam!')


add(2, 3)
spam()

