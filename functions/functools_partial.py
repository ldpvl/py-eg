from functools import partial

# partial is used to return a function with one (or more) of its argument "frozen/locked in"

import math

def distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    print(f'point 1: {point_1}, point 2: {point_2}')
    return math.hypot(x2 - x1, y2 - y1)


points = [(1, 2), (3, 4), (5, 6), (7, 8)]

my_point = (5, 5)

points_ordered_relative_to_my_point = sorted(points, key=partial(distance, my_point)) # passing my_point to point_1, note that my_point has to be a positional argument

print(points_ordered_relative_to_my_point)

print('-' * 10)

points_ordered_relative_to_my_point = sorted(points, key=partial(distance, point_2=my_point)) # passing my_point to point_2, note that it has to be a keyword argument

print(points_ordered_relative_to_my_point)

print('-' * 10)


def four_values(a, b, c, d):
    s = a + b + c + d
    print(f'{a} + {b} + {c} + {d} = {s}')
    return s

p = partial(four_values, 1, 1, d=1)

print(sorted([1, 2, 3], key=p)) # passing values from the list to c parameter