# Performing initialization or setup actions at the time of class definition is a classic use
# of metaclasses. Essentially, a metaclass is triggered at the point of a definition, at which
# point you can perform additional steps.

import operator

class StructTupleMeta(type):
    # The __init__() method in StructTupleMeta is only called once for each class that is
    # defined. The cls argument is the class that has just been defined. Essentially, the code
    # is using the _fields class variable to take the newly defined class and add some new
    # parts to it.
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))


class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []

    # Unlike __init__(), the __new__() method gets triggered before an instance is created.
    # Since tuples are immutable, it’s not possible to make any changes to them once they
    # have been created. An __init__() function gets triggered too late in the instance cre‐
    # ation process to do what we want. That’s why __new__() has been defined.
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))
        return super().__new__(cls, args)


class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']

class Point(StructTuple):
    _fields = ['x', 'y']


s = Stock('GOOG', 100, 1000.0)
print(s)