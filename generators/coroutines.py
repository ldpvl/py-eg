# Coroutines are similar to generators with a few differences. The main differences are:
#   generators are data producers
#   coroutines are data consumers

def string_contains(x):
    while True:
        string = yield
        if x in string:
            print(f'{x} is in string: {string}')
        else:
            print(f'{x} is not in string: {string}')


c = string_contains('ah')
next(c) # prime the coroutine
c.send('blah')
c.send('bluh')


def string_contains_2(x):
    while True:
        string = yield f'{x}_test'
        if x in string:
            print(f'{x} is in string: {string}')
        else:
            print(f'{x} is not in string: {string}')


c = string_contains_2('uh')
print(f"returned {next(c)}") # prime the coroutine
print(f"returned {c.send('blah')}")
print(f"returned {c.send('bluh')}")


def coroutine():
    a = yield 'a'
    print(f'sent 1st value {a}')
    b = yield 'b'
    print(f'sent 2nd value {b}')
    c = yield 'c'
    print(f'sent 3rd value {c}')
    print(f'final sum {(yield) + (yield)}')


c = coroutine()
print(f'returned value after priming coroutine: {next(c)}')
print(f'returned value after sending 1st value: {c.send(1)}')
print(f'returned value after sending 2nd value: {c.send(2)}')
print(f'returned value after sending 3rd value: {c.send(3)}')
print(f'returned value after sending 4th value: {c.send(4)}')
try:
    print(f'returned value after sending 4th value: {c.send(5)}')
except StopIteration:
    print('Last value has been sent')


def sum(x, y):
    yield (yield x) + (yield y)


s = sum(1, 2)
print(f'1st: {s.send(None)}') # priming coroutine, yield 1 which is passed value of x
print(f'2nd: {s.send(5)}') # yield 2 which is passed value of y
print(f'3rd: {s.send(6)}') # yield sum


