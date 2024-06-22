
# To use a metaclass, you would generally incorporate it into a top-level base class from
# which other objects inherit.

import traceback

from inspect import signature
import logging

class NoMixedCaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError(f'Attribute {name} is mixed-case')
        return super().__new__(cls, clsname, bases, clsdict)

class Root(metaclass=NoMixedCaseMeta):
    pass

class A(Root):
    def foo_bar(self): # Ok
        pass

try:
    class B(Root):
        def fooBar(self): # TypeError
            pass
except:
    traceback.print_exc()



class MatchSignaturesMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        sup = super(self, self)
        for name, value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue
            # Get the previous definition (if any) and compare the signatures
            prev_dfn = getattr(sup, name, None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    logging.warning(f'Signature mismatch in {value.__qualname__}. previous signature {prev_sig} != current signature {val_sig}')


# Example
class Root(metaclass=MatchSignaturesMeta):
    pass
class A(Root):
    def foo(self, x, y):
        pass
    def spam(self, x, *, z):
        pass
        # Class with redefined methods, but slightly different signatures

class B(A):
    def foo(self, a, b):
        pass
    def spam(self,x,z):
        pass