

import importlib
math = importlib.import_module('math')
print(math.sin(2))

# If you are working with packages, import_module() can also be used to perform relative
# imports. However, you need to give it an extra argument. For example:
# import importlib
# # Same as 'from . import b'
# b = importlib.import_module('.b', __package__)