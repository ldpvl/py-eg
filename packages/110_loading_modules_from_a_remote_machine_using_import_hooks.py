
# First, if you want to create a new module object, you use the imp.new_module() function.
# For example:

# >>> import imp
# >>> m = imp.new_module('spam')
# >>> m
# <module 'spam'>
# >>> m.__name__
# 'spam'
# >>>

# Module objects usually have a few expected attributes, including __file__ (the name
# of the file that the module was loaded from) and __package__ (the name of the enclosing
# package, if any).

# Second, modules are cached by the interpreter. The module cache can be found in the
# dictionary sys.modules. Because of this caching, it’s common to combine caching and
# module creation together into a single step. For example:
# >>> import sys
# >>> import imp
# >>> m = sys.modules.setdefault('spam', imp.new_module('spam'))
# >>> m
# <module 'spam'>
# >>>

# The main reason for doing this is that if a module with the given name already exists,
# you’ll get the already created module instead.

# >>> import math
# >>> m = sys.modules.setdefault('math', imp.new_module('math'))
# >>> m
# <module 'math' from '/usr/local/lib/python3.3/lib-dynload/math.so'>
# >>> m.sin(2)
# 0.9092974268256817
# >>> m.cos(2)
# -0.4161468365471424
# >>>

# errrrrrrr
