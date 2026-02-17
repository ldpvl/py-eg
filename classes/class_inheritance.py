

class Person:
    age = 0
    qualname = __qualname__

class Teacher(Person):
    school = 'FooBar'



teacher = Teacher()
print(teacher.qualname)

