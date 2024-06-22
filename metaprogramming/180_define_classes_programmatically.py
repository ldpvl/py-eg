
# class Spam(Base, metaclass=abc.ABCMeta, debug=True, typecheck=False):
# ...
#
# would translate to a new_class() call similar to this:
#
# Spam = types.new_class('Spam',
#                        (Base,),
#                        {'metaclass': abc.ABCMeta, 'debug': True, 'typecheck': False},
#                        lambda ns: ns.update(cls_dict))

# The fourth argument to new_class() is the most mysterious, but it is a function that
# receives the mapping object being used for the class namespace as input. This is normally
# a dictionary, but it’s actually whatever object gets returned by the __prepare__() method.

# One important aspect of the technique used in this recipe is its proper support for
# metaclasses. You might be inclined to create a class directly by instantiating a metaclass
# directly. For example:
#
# Stock = type('Stock', (), cls_dict)
#
# The problem is that this approach skips certain critical steps, such as invocation of the
# metaclass __prepare__() method. By using types.new_class() instead, you ensure
# that all of the necessary initialization steps get carried out. For instance, the callback
# function that’s given as the fourth argument to types.new_class() receives the map‐
# ping object that’s returned by the __prepare__() method.

import operator
import types
import sys


def custom_itemgetter(item):
    def get_something(an_iterable):
        print(f'returning {item} item of the tuple {an_iterable}')
        return an_iterable[item]
    return get_something




def named_tuple(classname, fieldnames):
    # Populate a dictionary of field property accessors

    # cls_dict = {name: property(operator.itemgetter(n))
    #             for n, name in enumerate(fieldnames)}

    cls_dict = {name: property(custom_itemgetter(n))  # the custom_itemgetter replaces the original operator.itemgetter(n)
                                                      # just so that it prints out some output so that it is easier to understand
                for n, name in enumerate(fieldnames)} # fget expects a function that returns the value of the managed attribute
                                                      # in this case, the function passed to fget expects the class instance
                                                      # object containing which in this case happens to be a tuple containing
                                                      # the values of the each field name/attribute

    print(f'cls_dict {cls_dict}')
    # Make a __new__ function and add to the class dict
    def __new__(cls, *args):
        if len(args) != len(fieldnames):
            raise TypeError(f'Expected {len(fieldnames)} arguments')
        return tuple.__new__(cls, args)

    cls_dict['__new__'] = __new__
    # Make the class
    cls = types.new_class(classname, (tuple,), {},
                          lambda ns: ns.update(cls_dict))

    # Set the module to that of the caller
    # a so-called “frame hack” involving sys._getframe() to
    # obtain the module name of the caller
    cls.__module__ = sys._getframe(1).f_globals['__name__']
    return cls


Stock = named_tuple('Stock', ['name', 'shares', 'price'])
s = Stock('GOOG', '100', 1000.0)
print(s)
print(s.name) # able to read the attribute due to fget being set as operator.itemgetter(n)
print(s.shares) # able to read the attribute due to fget being set as operator.itemgetter(n)
s.name = 'AMZN' # can't set as fset wasn't set