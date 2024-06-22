# To read a datafile, you might be inclined to write code that uses built-in I/O functions,
# such as open(). However, there are several problems with this approach.

# First, a package has very little control over the current working directory of the inter‐
# preter. Thus, any I/O operations would have to be programmed to use absolute file‐
# names. Since each module includes a __file__ variable with the full path, it’s not im‐
# possible to figure out the location, but it’s messy.
# Second, packages are often installed as .zip or .egg files, which don’t preserve the files in
# the same way as a normal directory on the filesystem. Thus, if you tried to use open()
# on a datafile contained in an archive, it wouldn’t work at all.

# The pkgutil.get_data() function is meant to be a high-level tool for getting a datafile
# regardless of where or how a package has been installed. It will simply “work” and return
# the file contents back to you as a byte string.

# The first argument to get_data() is a string containing the package name. You can
# either supply it directly or use a special variable, such as __package__. The second
# argument is the relative name of the file within the package. If necessary, you can nav‐
# igate into different directories using standard Unix filename conventions as long as the
# final directory is still located within the package.

# mypackage/
#   __init__.py
#   somedata.dat
#   spam.py


# spam.py
import pkgutil

data = pkgutil.get_data(__package__, 'somedata.dat')

# The resulting variable data will be a byte string containing the raw contents of the file.