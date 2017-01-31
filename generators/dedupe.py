# eg from python cookbook - removing duplicates from sequence while maintaining order
# nice blog post: https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
def dedupe(items, key=None):
    print('inside the generator')
    seen = set()
    for item in items:
        print('current item:', item, end=', ')
        value = item if key is None else key(item)
        print('assigned value', value, end=', ')
        if value not in seen:
            yield item
            print("back to loop, value:", value, end=', ')
            seen.add(value)
        print('end of loop cycle')


a = [{'x': 1, 'y': 2},
     {'x': 1, 'y': 3},
     {'x': 1, 'y': 2},
     {'x': 2, 'y': 3}]

print(list(dedupe(a, key=lambda d: (d['x'], d['y']))))
print('')
print(list(dedupe(a, key=lambda d: d['x'])))
print('')
print(list(dedupe(a, key=lambda d: d['y'])))
print('')
print(list(dedupe(a, key=lambda d: d['x'] + d['y'])))

print('')
print(list(dedupe(open('resources/dedupe.txt').read().splitlines())))
