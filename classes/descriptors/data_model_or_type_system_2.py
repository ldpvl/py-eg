from dataclasses import dataclass

# Base class. Uses a descriptor to set a value
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name # when the class attributes are first created, self.name is set to None
                         # but then the metaclass is used to set self.name to be the attribute variable name
                         # self.name will be used to reset the attribute variable's value as below

        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        print(f'about to set value "{value}" for instance {instance}') # Stock(ticker=<__main__.MaxSizedString object at 0x000002703DC8F0B8>, value=<__main__.UnsignedFloat object at 0x000002703DC8F780>)
        instance.__dict__[self.name] = value # this replaces Stock object instance's Descriptor instance with the underlying value
        print(f'have set value "{value}" for instance {instance}') # Stock(ticker='blah', value=<__main__.UnsignedFloat object at 0x000002703DC8F780>)

# Decorator for applying type checking
def Typed(expected_type, cls=None):
    if cls is None:
        return lambda cls: Typed(expected_type, cls)

    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError('expected ' + str(expected_type))

        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls


# Decorator for unsigned values
def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')

        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# Decorator for allowing sized values
def MaxSized(cls):
    super_init = cls.__init__

    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')

        super_init(self, name, **opts)

    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))

        super_set(self, instance, value)

    cls.__set__ = __set__

    return cls


@Typed(str)
class String(Descriptor):
    pass

@Typed(float)
class Float(Descriptor):
    pass

@Unsigned
class UnsignedFloat(Float):
    pass

@MaxSized
class MaxSizedString(String):
    pass


# A metaclass that applies checking
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        # Attach attribute names to the descriptors
        for key, value in methods.items():
            if isinstance(value, Descriptor): # look for methods that are class attributes
                value.name = key
        return type.__new__(cls, clsname, bases, methods)


@dataclass
class Stock(metaclass=checkedmeta): # metaclass logic is applied after class attributes but before decorator
    ticker: str = MaxSizedString(size=5) # @MaxSized String <= @Typed(str) Descriptor
    value: float = UnsignedFloat()


s = Stock(ticker='blah', value=5.0)
print(s)
print(s.ticker)
print(type(s.ticker))

# without the metaclass the below will be printed
# Stock(ticker=<__main__.MaxSizedString object at 0x00000280BD555F60>, value=<__main__.UnsignedFloat object at 0x00000280BD555710>)
# <__main__.MaxSizedString object at 0x00000280BD555F60>
# <class '__main__.MaxSizedString'>

# instead of
# Stock(ticker='blah', value=5.0)
# blah
# <class 'str'>