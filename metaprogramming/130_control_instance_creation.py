
import traceback


# Disallow the creation of instances
class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")


class Spam(metaclass=NoInstances):
    def __init__(self, name):
        self.name = name


try:
    s = Spam('test')
except:
    traceback.print_exc()




# allow singleton instance
class Singleton(type):
    # self is a class instance of Spam
    def __init__(self, *args, **kwargs):
        print(f'Init Singleton for class object {self.__qualname__}')
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print(f'Call method gets called before an {self.__qualname__} instance is initialized')
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Spam(metaclass=Singleton):
    def __init__(self, name):
        print('Creating Spam')
        self.name = name


print(f'Spam attributes before first init: {vars(Spam)}')
a = Spam('a')
print(f'Spam attributes after first init: {vars(Spam)}')
b = Spam('b')
c = Spam('c')

print(f'a is b: {a is b}')
print(f'a is c: {a is c}')



# cached instances
import weakref
class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj


class Spam(metaclass=Cached):
    def __init__(self, name):
        print(f'Creating cached Spam({name!r})')
        self.name = name


a = Spam('a')
b = Spam('b')
c = Spam('a')

print(f'a is b: {a is b}')
print(f'a is c: {a is c}')
