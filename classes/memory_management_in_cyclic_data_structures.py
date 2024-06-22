


# The reason is that Python’s garbage collection is based on simple reference counting.
# When the reference count of an object reaches 0, it is immediately deleted. For
# cyclic data structures, however, this never happens. Thus, in the last part of the example,
# the parent and child nodes refer to each other, keeping the reference count nonzero.


import gc


# Class just to illustrate when deletion occurs
class Data:
    def __del__(self):
        print('Data.__del__')

# Node class involving a cycle
class Node:
    def __init__(self):
        self.data = Data()
        self.parent = None
        self.children = []

    # NEVER DEFINE LIKE THIS
    # Only here to illustrate pathological behavior
    def __del__(self):
        del self.data
        del self.parent
        del self.children

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


a = Node()
a.add_child(Node())
# Note that, the problem with finalizers, which was described in the original proposal, has been fixed since Python 3.4. You can read about it in the PEP 442.
del a # No message (not collected)
gc.collect() # No message (not collected)


import weakref
a = Node()
a_ref = weakref.ref(a)
print(f'a_ref: {a_ref}')
print(a_ref())
del a
print(a_ref())
