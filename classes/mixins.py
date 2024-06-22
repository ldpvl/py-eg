# You have a collection of generally useful methods that you would like to make available
# for extending the functionality of other class definitions. However, the classes where
# the methods might be added aren’t necessarily related to one another via inheritance.
# Thus, you can’t just attach the methods to a common base class.

# First, mixin classes are never meant to be instantiated directly. For example, none of the
# classes in this recipe work by themselves. They have to be mixed with another class that
# implements the required mapping functionality. Similarly, the ThreadingMixIn from
# the socketserver library has to be mixed with an appropriate server class—it can’t be
# used all by itself.

# Second, mixin classes typically have no state of their own. This means there is no
# __init__() method and no instance variables. In this recipe, the specification of
# __slots__ = () is meant to serve as a strong hint that the mixin classes do not have
# their own instance data.

class SetOnceMappingMixin:
    '''
    Only allow a key to be set once.
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)

class StringKeysMappingMixin:
    '''
    Restrict keys to strings only
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key, value)

from traceback import print_exc
from collections import OrderedDict

class StringOrderedDict(StringKeysMappingMixin, SetOnceMappingMixin, OrderedDict):
    pass

d = StringOrderedDict()
d['x'] = 23

try:
    d[1] = 1 # TypeError: keys must be strings
except:
    print_exc()

try:
    d['x'] = 1 # KeyError: 'x already set'
except:
    print_exc()

# If you are thinking about defining a mixin class that has an __init__() method and
# instance variables, be aware that there is significant peril associated with the fact that
# the class doesn’t know anything about the other classes it’s going to be mixed with. Thus,
# any instance variables created would have to be named in a way that avoids name clashes.
# In addition, the __init__() method would have to be programmed in a way that prop‐
# erly invokes the __init__() method of other classes that are mixed in. In general, this
# is difficult to implement since you know nothing about the argument signatures of the
# other classes. At the very least, you would have to implement something very general
# using *arg, **kwargs. If the __init__() of the mixin class took any arguments of its
# own, those arguments should be specified by keyword only and named in such a way
# to avoid name collisions with other arguments. Here is one possible implementation of
# a mixin defining an __init__() and accepting a keyword argument:

class RestrictKeysMixin:
    def __init__(self, *args, _restrict_key_type, **kwargs):
        self.__restrict_key_type = _restrict_key_type
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not isinstance(key, self.__restrict_key_type):
            raise TypeError('Keys must be ' + str(self.__restrict_key_type))
        super().__setitem__(key, value)


class RDict(RestrictKeysMixin, dict):
    pass


f = RDict(name='Dave', n=37, _restrict_key_type=str)

try:
    f[1] = 1 # TypeError: Keys must be <class 'str'>
except:
    print_exc()