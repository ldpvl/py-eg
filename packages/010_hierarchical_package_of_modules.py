
# More often that not, it’s fine to just leave the __init__.py files empty. However, there are
# certain situations where they might include code. For example, an __init__.py file can
# be used to automatically load submodules like this:

# # graphics/formats/__init__.py
# from . import jpg
# from . import png

# For such a file, a user merely has to use a single import graphics.formats instead of
# a separate import for graphics.formats.jpg and graphics.formats.png.

# Other common uses of __init__.py include consolidating definitions from multiple files
# into a single logical namespace, as is sometimes done when splitting modules.

# Astute programmers will notice that Python 3.3 still seems to perform package imports
# even if no __init__.py files are present. If you don’t define __init__.py, you actually
# create what’s known as a “namespace package,” which is described in Recipe 10.5. All
# things being equal, include the __init__.py files if you’re just starting out with the cre‐
# ation of a new package.