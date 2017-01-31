class Magnitude(object):
    def __init__(self, initval=None, name=None):
        self.val = initval
        self.name = name

    def __get__(self, instance, type):
        print('Retrieving:', self.name)
        return self.name

    def __set__(self, instance, value):
        try:
            float(value)
            instance.__dict__[self.name] = value
            print('Setting value', value, 'for', self.name)
        except ValueError:
            raise ValueError('Value must be a number but given', value, 'instead')


class Foo:
    x = Magnitude(name='earthquake')
    y = Magnitude(name='supernova')

    def __init__(self, description, earthquake, supernova):
        self.description = description
        self.earthquake = earthquake
        self.supernova = supernova

foo = Foo('Bar', 5, 'a')
foo.x
foo.y
