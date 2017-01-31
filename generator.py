# nice blog post: https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
def increment(base=0):
    value = base
    while True:
        print("beginning of loop cycle, value:", value, end=', ')
        addend = yield value
        print("back to loop", end=', ')
        value += 1 if addend is None else addend
        print("end of loop cycle, value:", value, end=', ')


g = increment()
print('initialised the generator')
print("yielded 1st value:", next(g))
print("yielded 2nd value:", g.send(3))
print("yielded 3rd value:", g.send(5))
print("yielded 4th value:", next(g))
print("yielded 5th value:", next(g))
print("yielded 6th value:", next(g))
print("yielded 7th value:", next(g))
print("yielded 8th value:", g.send(10))


def two_ranges_combined(x):
    yield from range(x)
    yield from range(x, -1, -1)

print('\ncombined range', list(two_ranges_combined(5)))
