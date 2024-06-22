
# Before using exec(), you might ask yourself if other alternatives are
# available. Many problems where you might consider the use of exec() can be replaced
# by closures, decorators, metaclasses, or other metaprogramming features.

from traceback import print_exc
from pprint import pformat


def test():
    a = 13
    exec('b = a + 1')
    print(b)


try:
    test()
except:
    print_exc() # throws NameError: global name 'b' is not defined


def test2():
    a = 13
    loc = locals()
    exec('b = a + 1')
    b = loc['b']
    print(b)


print(f'test2:')


def test3():
    x = 2
    loc = locals()
    print('before: ', pformat(loc))
    exec('x += 1')
    print('after: ', pformat(loc))
    print('x = ', x)


print('test3:')
test3()

# Each time it is invoked, locals() will take the current value of local variables and overwrite
# the corresponding entries in the dictionary.


def test4():
    x = 0
    loc = locals()
    print(loc)
    exec('x += 1')
    print(loc)
    locals()
    print(loc)

print('test4:')
test4()


# As an alternative to using locals(), you might make your own dictionary and pass it
# to exec(). For most uses of exec(), this is probably good practice. You just need to make sure that
# the global and local dictionaries are properly initialized with names that the executed
# code will access.

def test5():
    a = 13
    loc = {'a': a}
    glb = {}
    exec('b = a + 1', glb, loc)
    b = loc['b']
    print(b)


print('test5:')
test5()