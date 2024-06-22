
# There are two common ways to get new directories added to sys.path. First, you can
# add them through the use of the PYTHONPATH environment variable.
# >>> import sys
# >>> sys.path
# ['', '/some/dir', '/other/dir', ...]

# You can sometimes work around the problem of hardcoded directories if you carefully
# construct an appropriate absolute path using module-level variables, such as
# __file__. For example:
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, abspath(dirname('__file__'), 'src'))

# The second approach is to create a .pth file that lists the directories like this:
# myapplication.pth
# /some/dir
# /other/di

# This .pth file needs to be placed into one of Python’s site-packages directories, which are
# typically located at /usr/local/lib/python3.3/site-packages or ~/.local/lib/python3.3/site-
# packages. On interpreter startup, the directories listed in the .pth file will be added to
# sys.path as long as they exist on the filesystem. Installation of a .pth file might require
# administrator access if it’s being added to the system-wide Python interpreter.

# Although .pth files for configuring the path must appear in site-packages, they
# can refer to any directories on the system that you wish. Thus, you can elect to have
# your code in a completely different set of directories as long as those directories are
# included in a .pth file.