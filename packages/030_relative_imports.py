# The downside of using an absolute name, such as mypackage.A, is that it hardcodes the
# top-level package name into your source code. This, in turn, makes your code more
# brittle and hard to work with if you ever want to reorganize it. For example, if you ever
# changed the name of the package, you would have to go through all of your files and fix
# the source code.

# Similarly, hardcoded names make it difficult for someone else to move
# the code around. For example, perhaps someone wants to install two different versions
# of a package, differentiating them only by name. If relative imports are used, it would
# all work fine, whereas everything would break with absolute names.

# Finally, it should be noted that relative imports only work for modules that are located
# inside a proper package. In particular, they do not work inside simple modules located
# at the top level of scripts. They also won’t work if parts of a package are executed directly
# as a script. For example:
# % python3 mypackage/A/spam.py # Relative imports fail
# On the other hand, if you execute the preceding script using the -m option to Python,
# the relative imports will work properly. For example:
# % python3 -m mypackage.A.spam # Relative imports work

# from . import grok
# from ..B import bar