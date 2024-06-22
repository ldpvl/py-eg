class Magnitude(object):
    def __init__(self, initval=None, name=None):
        self.val = initval
        self.name = name

    def __get__(self, instance, type):
        # the if statement is to account for the distinction
        # between instance variables and class variables
        if instance is None:
            return self
        else:
            print('Retrieving:', self.name)
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        try:
            float(value)
            instance.__dict__[self.name] = value
            print('Setting value', value, 'for', self.name)
        except ValueError:
            raise ValueError('Value must be a number but given', value, 'instead')

    def __del__(self, instance):
        del instance.__dict__[self.name]


class Foo:
    x = Magnitude(name='earthquake') # can only be defined at the class level, not on a per-instance basis
    y = Magnitude(name='supernova')

    def __init__(self, description, earthquake, supernova):
        self.description = description
        self.earthquake = earthquake
        self.supernova = supernova

foo = Foo('Bar', 5, 'a')
print(f'Foo.x: {Foo.x} of type {type(Foo.x)}')
print(f'foo.x: {foo.x} of type {type(foo.x)}')
foo.x # Retrieving: earthquake
foo.y # Retrieving: supernova
