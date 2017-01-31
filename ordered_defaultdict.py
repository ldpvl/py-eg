from collections import OrderedDict
from collections import defaultdict


class OrderedDefaultDict(OrderedDict, defaultdict):
    pass


analyzed_symbols = OrderedDefaultDict()
analyzed_symbols.default_factory = lambda: int(0)


def add_to_analyzed_symbols(symbol_details):
    analyzed_symbols[symbol_details[0]] += 1


test_data = ['c', 'd', 'b', 'b', 'a', 'b', 'e', 'e', 'e', 'a']

for x in test_data:
    add_to_analyzed_symbols(x)

for x, y in analyzed_symbols.items():
    print(x, y, sep=' count is ')
