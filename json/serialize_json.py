class Person:
    def __init__(self, age, height, sex, gender):
        self.age = age
        self.height = height
        self.sex = sex
        self.gender = gender

classes = {
    'Person': Person
}

def serliaze_object(obj):
    d = {'__classname__': type(obj).__name__}
    d.update(vars(obj))
    return d

def deserialize_object(d):
    class_name = d.pop('__classname__', None)
    if class_name:
        cls = classes[class_name]
        obj = cls.__new__(cls)
        for key, value in d.items():
            setattr(obj, key, value)
        return obj
    else:
        raise Exception("No __classname__ value found.")

john = Person(25, 180, 'male', 'woman')

s_john = serliaze_object(john)

d_s_john = deserialize_object(s_john)

print(s_john)
print(d_s_john)
