
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args) # call the add function
    # Invoke the callback with the result
    callback(result) # result_queue.put(result)

from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func # this gonna be the add function
        self.args = args


def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args) # test() is a generator
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result) # on init, None is sent to test() generator to prime it by instantiating first Async object
                                   # subsequently, when a proper result (from add function) is retrieved from the result_queue
                                   # it is sent to f (test() generator), the generator then moves to the next yield and waits for
                                   # the next f.send()
                apply_async(a.func, a.args, callback=result_queue.put) # a is an instance of Async
            except StopIteration:
                break
    return wrapper


def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')


test()