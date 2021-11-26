
# A read-only attribute as a property that only gets computed on access.
# However, once accessed, you’d like the value to be cached and not recomputed on each
# access.

class lazyproperty:
    def __init__(self, func):
        self.func = func

    # When a descriptor is placed into a class
    # definition, its __get__() , __set__() , and __delete__() methods get triggered on at‐
    # tribute access. However, if a descriptor only defines a __get__() method, it has a much
    # weaker binding than usual. In particular, the __get__() method only fires if the attribute
    # being accessed is not in the underlying instance dictionary.

    # The lazyproperty class exploits this by having the __get__() method store the com‐
    # puted value on the instance using the same name as the property itself. By doing this,
    # the value gets stored in the instance dictionary and disables further computation of the
    # property.
    def __get__(self, instance, cls):
        # the if statement is to account for the distinction
        # between instance variables and class variables
        if instance is None:
            return self
        else:
            print(f'Setting value for {instance}')
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
        print(f'Initialised circle with radius {radius}')

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius


c = Circle(4.0)
print(f'===== {vars(c)}')
print(c.area) # prints Computing area, the value is set once the function is called the first time
print(f'===== {vars(c)}')
print(c.area) # does not print Computing area, means cached value is returned and the property is not invoked because
              # the variable area already exists
del c.area
print(f'===== {vars(c)}')
print(c.area) # prints Computing area, the value is set once again because the variable area was deleted earlier
print(f'===== {vars(c)}')


# c.area in this case is mutable which can be undesirable
# below is a less efficient implementation which prevents overriding c.area
# However, a disadvantage is that all get operations have to be routed through the prop‐
# erty’s getter function. This is less efficient than simply looking up the value in the in‐
# stance dictionary
def lazyproperty(func):
    name = '_lazy_' + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy


class Circle:
    def __init__(self, radius):
        self.radius = radius
        print(f'Initialised circle with radius {radius}')

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2


c = Circle(4.0)
print(f'===== {vars(c)}')
print(c.area) # prints Computing area, the value is set once the function is called the first time
print(f'===== {vars(c)}')
print(c.area) # does not print Computing area, means cached value is returned and the property is not invoked because
# the variable area already exists
c.area = 10 # throws AttributeError