# Assuming that the decorator has been implemented properly using @wraps, you can usually gain access to the original
# function by accessing the __wrapped__ attribute.
# mileage may vary
# not all decorators utilize @wraps, and thus, they may
# not work as described. In particular, the built-in decorators @staticmethod and @class
# method create descriptor objects that don’t follow this convention (instead, they store
# the original function in a __func__ attribute)


from functools import wraps


def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 1')
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 2')
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def add(x, y):
    return x + y


print('both decorators')
print(add(2, 3))
print('removed first decorator')
print(add.__wrapped__(2, 3))
print('removed both decorators')
print(add.__wrapped__.__wrapped__(2, 3))