# When creating instances of a class, you want to return a cached reference to a previous
# instance created with the same arguments (if any).
# The problem being addressed in this recipe sometimes arises when you want to ensure
# that there is only one instance of a class created for a set of input arguments. Practical
# examples include the behavior of libraries, such as the logging module, that only want
# to associate a single logger instance with a given name.

import logging
a = logging.getLogger('foo')
b = logging.getLogger('bar')
print(f'a is b {a is b}')
c = logging.getLogger('foo')
print(f'a is c {a is c}')


class Spam:
    def __init__(self, *args, **kwargs):
        # to prevent users directly instantiating Spam class which will bypass caching
        raise RuntimeError("Can't instantiate directly")

    # Alternate constructor
    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name
        return self


import weakref


# A cached manager implementation also helps to decouple the init process away from the Spam class that way init is not
# called every time a new Spam instance is created

class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam._new(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s

m = CachedSpamManager()
a = m.get_spam('foo')
b = m.get_spam('foo')
c = m.get_spam('bar')

print(f'a is {a}, a is b {a is b}, b is c {b is c}')
