# apply the @wraps decorator from the functools library to the underlying wrapper function to preserve important metadata
# such as the name, doc string, annotations, and calling signature

# @timethis
# def countdown(n):
#   ...
#
# is equivalent to
#
# def countdown(n):
#   ...
#
# countdown = timethis(countdown)

import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper

def timethisnowraps(func):
    '''
    Decorator that reports the execution time.
    '''

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper

@timethis
def countdown(n:int):
    '''
    Counts down
    '''
    while n > 0:
        n -= 1

@timethisnowraps
def countdownnowraps(n:int):
    '''
    Counts down
    '''
    while n > 0:
        n -= 1

countdown(1000000)
print('With wraps')
print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)

print('No wraps')
print(countdownnowraps.__name__)
print(countdownnowraps.__doc__)
print(countdownnowraps.__annotations__)
