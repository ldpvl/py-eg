
# Normally, to write a context manager, you define a class with an __enter__() and
# __exit__() method, like this:

import time

class timethis:
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_ty, exc_val, exc_tb):
        end = time.time()
        print('{}: {}'.format(self.label, end - self.start))


# @contextmanager is really only used for writing self-contained context-management
# functions. If you have some object (e.g., a file, network connection, or lock) that needs
# to support the with statement, you still need to implement the __enter__() and
# __exit__() methods separately.


from contextlib import contextmanager

@contextmanager
def timethis(label):
    start = time.time()

    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))



with timethis('counting'):
    n = 10000000
    while n > 0:
        n -= 1
