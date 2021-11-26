def add(x, y):
    return x + y

def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)
    # Invoke the callback with the result
    callback(result)

def print_sequence(sequence, result):
    print(f'[{sequence}] Got: {result}')


def make_handler_coroutine():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print_sequence(sequence, result)


handler = make_handler_coroutine()
next(handler) # go to yield
print('Coroutine')
apply_async(add, (1, 2), callback=handler.send) # use send method to send arguments to coroutine
apply_async(add, (4, 2), callback=handler.send) # use send method to send arguments to coroutine



def make_handler_closure():
    sequence = 0

    def handler(result):
        nonlocal sequence
        sequence += 1
        print_sequence(sequence, result)

    return handler


handler = make_handler_closure()
print('Closure')
apply_async(add, (1, 2), callback=handler)
apply_async(add, (3, 2), callback=handler)


class ResultHandler:
    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print_sequence(self.sequence, result)


handler = ResultHandler()
print('Class')
apply_async(add, (1, 2), callback=handler.handler)
apply_async(add, (3, 3), callback=handler.handler)


class Sequence:
    def __init__(self):
        self.sequence = 0

def handler(result, sequence):
    sequence.sequence += 1
    print_sequence(sequence.sequence, result)


from functools import partial
print('Partial')
sequence = Sequence()
apply_async(add, (1, 2), callback=partial(handler, sequence=sequence))
apply_async(add, (4, 4), callback=partial(handler, sequence=sequence))
