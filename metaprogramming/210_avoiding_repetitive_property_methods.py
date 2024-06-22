
def typed_property(name, expected_type): # this is a closure
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError('{} must be a {}'.format(name, expected_type))

        setattr(self, storage_name, value)

    return prop


class Person:
    name = typed_property('name', str)
    age = typed_property('age', int)

    def __init__(self, name, age):
        self.name = name
        self.age = age



p = Person('Foo', 1)
print(p.name)
print(p.age)
print(vars(p))


from functools import partial

String = partial(typed_property, expected_type=str)
Integer = partial(typed_property, expected_type=int)


class Person:
    name = String('name')
    age = Integer('age')

    def __init__(self, name, age):
        self.name = name
        self.age = age

print(p.name)
print(p.age)
print(vars(p))
