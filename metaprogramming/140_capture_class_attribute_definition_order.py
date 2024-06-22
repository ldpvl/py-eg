
# automatically record the order in which attributes and methods are defined
# inside a class body so that you can use it in various operations (e.g., serializing, mapping

from collections import OrderedDict
from dataclasses import dataclass

class NoDupOrderedDict(OrderedDict):
    def __init__(self, clsname):
        self.clsname = clsname
        super().__init__()

    def __setitem__(self, name, value):
        if name in self:
            raise TypeError('{} already defined in {}'.format(name, self.clsname))
        super().__setitem__(name, value)


# A set of descriptors for various types
class Typed:
    _expected_type = type(None)

    def __init__(self, name=None):
        self._name = name # initially gets initialized as None, then it gets set by OrderedMeta metaclass which can be
                          # used for some purpose, though in this example it's not used for anything in particular

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError('Expected ' + str(self._expected_type))
        instance.__dict__[self._name] = value

class Integer(Typed):
    _expected_type = int

class Float(Typed):
    _expected_type = float

class String(Typed):
    _expected_type = str


# Metaclass that uses a NoDupOrderedDict for class body
# The entire key to this recipe is the __prepare__() method, which is defined in the
# OrderedMeta metaclass. This method is invoked immediately at the start of a class def‐
# inition with the class name and base classes. It must then return a mapping object to
# use when processing the class body. By returning an OrderedDict instead of a normal
# dictionary, the resulting definition order is easily captured.
#
# A final important part of this recipe concerns the treatment of the modified dictionary
# in the metaclass __new__() method. Even though the class was defined using an alter‐
# native dictionary, you still have to convert this dictionary to a proper dict instance
# when making the final class object. This is the purpose of the d = dict(clsdict)
# statement.
class OrderedMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        print(f'__new__ is invoked for {clsname} with class dictionary {clsdict}')
        d = dict(clsdict)
        order = []

        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name
                print(f"Set descriptor {value.__class__.__name__} name as {name}")
                order.append(name)

        d['_order'] = order
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(cls, clsname, bases):
        print(f'__prepare__ method is invoked immediately at the start of the class {clsname} '
              f'definition and base classes {bases}')
        return NoDupOrderedDict(clsname)


class Structure(metaclass=OrderedMeta):
    def as_csv(self):
        return ','.join(str(getattr(self,name)) for name in self._order)


# Example use
class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


s = Stock('GOOG', 100, 1000.0)
print(s.as_csv())


class WithDupe(Structure):
    name = String()
    name = String()


s = WithDupe()