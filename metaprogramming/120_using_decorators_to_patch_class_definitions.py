
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

# Example use
@log_getattribute
class A:
    def __init__(self,x):
        self.x = x

    def spam(self):
        pass


a = A(50)
a.x

a.spam()


# Class decorators can often be used as a straightforward alternative to other more ad‐
# vanced techniques involving mixins or metaclasses.
# This works, but to understand it, you have to have some awareness of the method res‐
# olution order, super(), and other aspects of inheritance, as described in Recipe 8.7. In
# some sense, the class decorator solution is much more direct in how it operates, and it
# doesn’t introduce new dependencies into the inheritance hierarchy. As it turns out, it’s
# also just a bit faster, due to not relying on the super() function.
# If you are applying multiple class decorators to a class, the application order might
# matter. For example, a decorator that replaces a method with an entirely new imple‐
# mentation would probably need to be applied before a decorator that simply wraps an
# existing method with some extra logic.

class LoggedGetattribute:
    def __getattribute__(self, name):
        print('getting:', name)
        return super().__getattribute__(name)

# Example:
class A(LoggedGetattribute):
    def __init__(self,x):
        self.x = x

    def spam(self):
        pass

a = A(40)
a.x

a.spam()
