# To unify separate directories under a common namespace, you organize the code just
# like a normal Python package, but you omit __init__.py files in the directories where
# the components are going to join together.

# The mechanism at work here is a feature known as a “namespace package.” Essentially,
# a namespace package is a special kind of package designed for merging different direc‐
# tories of code together under a common namespace, as shown. For large frameworks,
# this can be useful, since it allows parts of a framework to be broken up into separately
# installed downloads. It also enables people to easily make third-party add-ons and other
# extensions to such frameworks.

# foo-package/
#   spam/
#       blah.py

# bar-package/
#   spam/
#       grok.py

# >>> import sys
# >>> sys.path.extend(['foo-package', 'bar-package'])
# >>> import spam.blah
# >>> import spam.grok

# The key to making a namespace package is to make sure there are no __init__.py files
# in the top-level directory that is to serve as the common namespace. The missing
# __init__.py file causes an interesting thing to happen on package import. Instead of
# causing an error, the interpreter instead starts creating a list of all directories that happen
# to contain a matching package name. A special namespace package module is then
# created and a read-only copy of the list of directories is stored in its __path__ variable.
# For example:
# >>> import spam
# >>> spam.__path__
# _NamespacePath(['foo-package/spam', 'bar-package/spam'])
# >>>