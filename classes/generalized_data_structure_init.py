
# To avoid highly repetitive and boilerplate __init__() functions in similar data structures

# One possible choice is to use keyword arguments as a means for adding additional
# attributes to the structure not specified in _fields

# Though this method has one downside of not making code documentation clear

class Structure:
    # Class variable that specifies expected fields
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set the arguments
        # The use of setattr instead of accessing the instance __dict__ to not make assumptions about the implementation
        # of a subclass. If a subclass decided to use __slots__ or wrap a specific attribute with a
        # property (or descriptor), directly accessing the instance dictionary would break. The
        # solution has been written to be as general purpose as possible and not to make any
        # assumptions about subclasses.
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Set the additional arguments (if any)
        extra_args = kwargs.keys() - self._fields

        for name in extra_args:
            setattr(self, name, kwargs.pop(name))

        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))


class Stock(Structure):
    _fields = ['name', 'shares', 'price']

s1 = Stock('ACME', 50, 91.1)
s2 = Stock('ACME', 50, 91.1, date='8/2/2012')

print(vars(s1))
print(vars(s2))
