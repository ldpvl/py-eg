
import traceback
import inspect

from inspect import Signature, Parameter


# Make a signature for a func(x, y=42, *, z=None)
params = [Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
          Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=42),
          Parameter('z', Parameter.KEYWORD_ONLY, default=None)]

sig = Signature(params)
print(sig)

def func(*args, **kwargs):
    bound_values = sig.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
        print(name, value)


func(1, 2, z=3)
print('=' * 9)

func(1)
print('=' * 9)

func(1, z=3)
print('=' * 9)

try:
    func(1, 2, 3, 4)
except:
    # throws TypeError: too many positional arguments
    traceback.print_exc()

try:
    func(y=2)
except:
    # throws TypeError: missing a required argument: 'x'
    traceback.print_exc()

try:
    func(1, y=2, x=3)
except:
    # throws TypeError: multiple values for argument 'x'
    traceback.print_exc()


################################################################
def make_sig(*names):
    params = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
              for name in names]
    return Signature(params)


class Structure:
    __signature__ = make_sig()
    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)


class Stock(Structure):
    __signature__ = make_sig('name', 'shares', 'price')


class Point(Structure):
    __signature__ = make_sig('x', 'y')


print(f'Signature of {Stock.__name__}: {inspect.signature(Stock)}')

s1 = Stock('ACME', 100, 1000)

try:
    s2 = Stock('ACME', 100)
except:
    # throws TypeError: missing a required argument: 'price'
    traceback.print_exc()

try:
    s3 = Stock('ACME', 100, 1000, shares=5)
except:
    # TypeError: multiple values for argument 'shares'
    traceback.print_exc()



################################################################


class StructureMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsdict['__signature__'] = make_sig(*clsdict.get('_fields', [])) # make signature from the list of fields
        return super().__new__(cls, clsname, bases, clsdict)


class Structure(metaclass=StructureMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs) # self.__signature__ is created by the metaclass StructureMeta
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)

class Stock2(Structure):
    _fields = ['name', 'shares', 'price']


class Point2(Structure):
    _fields = ['x', 'y']



print(f'Signature of {Stock2.__name__}: {inspect.signature(Stock)}')
