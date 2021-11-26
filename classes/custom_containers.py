import collections


class A(collections.Iterable):
    pass


try:
    a = A()
except TypeError:
    print(
        "The special feature about inheriting from collections.Iterable is that it ensures you implement all of the "
        "required special methods. If you don't, you'll get an error upon instantiation")
