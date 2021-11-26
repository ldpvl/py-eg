
# Base class. Uses a descriptor to set a value
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name

        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


# Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected ' + str(self.expected_type))

        super().__set__(instance, value)


# Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')

        super().__set__(instance, value)


class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')

        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))

        super().__set__(instance, value)


class MaxValue(Descriptor):
    def __init__(self, name=None, **opts):
        if 'max_value' not in opts:
            raise TypeError('missing max_value option')

        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if value > self.max_value:
            raise ValueError(f'value must be < {self.max_value}')

        super().__set__(instance, value)


# Data model / type system:
class Integer(Typed):
    expected_type = int

class UnsignedInteger(Integer, Unsigned):
    pass

class UnsignedCappedInteger(Integer, Unsigned, MaxValue):
    pass

class Float(Typed):
    expected_type = float

class UnsignedFloat(Float, Unsigned):
    pass

class String(Typed):
    expected_type = str

class SizedString(String, MaxSized):
    pass


from dataclasses import dataclass

@dataclass
class Top500Stock:
    position: int = UnsignedCappedInteger('position', max_value=500)
    ticker: str = SizedString('ticker', size=8)

s = Top500Stock(499, 'xyz')
print(s.position)
print(s.ticker)


# There are some techniques that can be used to simplify the specification of constraints
# in classes. One approach is to use a class decorator, like this:

# Class decorator to apply constraints
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate


print(f'UnsignedFloat is an instance of Descriptor: {isinstance(UnsignedFloat, Descriptor)}')
print(f'UnsignedFloat() is an instance of Descriptor: {isinstance(UnsignedFloat(), Descriptor)}')


@check_attributes(position=UnsignedCappedInteger(max_value=100),
                  ticker=SizedString(size=8),
                  price=UnsignedFloat)
class Top100Stock:
    def __init__(self, position, ticker, price):
        self.position = position
        self.ticker = ticker
        self.price = price


print(Top100Stock(position=99, ticker='xyz', price=139.0))


# A metaclass that applies checking
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        # Attach attribute names to the descriptors
        for key, value in methods.items(): # methods are class attributes
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


@dataclass
class Top20Stock(metaclass=checkedmeta):
    position: int = UnsignedCappedInteger(max_value=500) # no longer needed to specify 'name' argument
    ticker: str = SizedString(size=8)


print(Top20Stock(4, 'xyz'))