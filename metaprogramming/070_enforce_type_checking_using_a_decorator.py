from inspect import signature
from functools import wraps


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        # First, one aspect of decorators is that they only get applied once, at the time of function
        # definition. In certain cases, you may want to disable the functionality added by a dec‐
        # orator. To do this, simply have your decorator function return the function unwrapped.
        # In the solution, the following code fragment returns the function unmodified if the
        # value of the global __debug__ variable is set to False (as is the case when Python executes
        # in optimized mode with the -O or -OO options to the interpreter):
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)


        # In this partial binding, you will notice that missing arguments are simply ignored
        # However, the most important part of the binding
        # is the creation of the ordered dictionary bound_types.arguments. This dictionary maps
        # the argument names to the supplied values in the same order as the function signature.
        # In the case of our decorator, this mapping contains the type assertions that we’re going
        # to enforce.
        # eg: OrderedDict([('x', <class 'int'>), ('z', <class 'int'>)])
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs) # bind() is like bind_partial() except that it does not allow for missing arguments
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))

            return func(*args, **kwargs)
        return wrapper
    return decorate

# A somewhat subtle aspect of the solution is that the assertions do not get applied to
# unsupplied arguments with default values. For example, this code works, even though
# the default value of items is of the “wrong” type

# A final point of design discussion might be the use of decorator arguments versus func‐
# tion annotations. For example, why not write the decorator to look at annotations like
# this?
#
# @typeassert
# def spam(x:int, y, z:int = 42):
#     print(x,y,z)
#
# One possible reason for not using annotations is that each argument to a function can
# only have a single annotation assigned. Thus, if the annotations are used for type as‐
# sertions, they can’t really be used for anything else. Likewise, the @typeassert decorator
# won’t work with functions that use annotations for a different purpose. By using deco‐
# rator arguments, as shown in the solution, the decorator becomes a lot more general
# purpose and can be used with any function whatsoever—even functions that use
# annotations.


@typeassert(int, z=int)
def add(x, y, z):
    return x + y + z


try:
    add(1, '2', 3)
except Exception as e:
    print(e)


try:
    add(1, 2, '3')
except Exception as e:
    print(e)
