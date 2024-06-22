# Definitions of # __eq__() and __lt__() are provided to compare .
# This minimum definition is all that is required to make all of the other comparison operations work.

from functools import total_ordering

@total_ordering
class Apple:
    def __init__(self, weight):
        self.weight = weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight


apple_1 = Apple(5)
apple_2 = Apple(5)
apple_3 = Apple(6)
print(apple_1 > apple_2)
print(apple_1 == apple_2)
print(apple_1 >= apple_2)
print(apple_1 > apple_3)
