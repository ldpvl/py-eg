# eg from python cookbook - Combining Multiple Mappings into a Single Mapping
from collections import ChainMap

a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}

merged = ChainMap(a, b)

print(merged['x'])  # prints 1
a['x'] = 42

print(merged['x'])  # prints 42
a['x'] = 42
