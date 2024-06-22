
# An RLock or re-entrant lock
# object is a lock that can be acquired multiple times by the same thread. It is primarily
# used to implement code based locking or synchronization based on a construct known
# as a “monitor.” With this kind of locking, only one thread is allowed to use an entire
# function or the methods of a class while the lock is held. For example, you could im‐
# plement the SharedCounter class like this:

# In this variant of the code, there is just a single class-level lock shared by all instances
# of the class. Instead of the lock being tied to the per-instance mutable state, the lock is
# meant to synchronize the methods of the class. Specifically, this lock ensures that only
# one thread is allowed to be using the methods of the class at once. However, unlike a
# standard lock, it is OK for methods that already have the lock to call other methods that
# also use the lock (e.g., see the decr() method).

# One feature of this implementation is that only one lock is created, regardless of how
# many counter instances are created. Thus, it is much more memory-efficient in situa‐
# tions where there are a large number of counters. However, a possible downside is that
# it may cause more lock contention in programs that use a large number of threads and
# make frequent counter updates.

import threading

class SharedCounter:
    '''
    A counter object that can be shared by multiple threads.
    '''
    _lock = threading.RLock()

    def __init__(self, initial_value=0):
        self._value = initial_value

    def incr(self, delta=1):
        '''
        Increment the counter with locking
        '''
        with SharedCounter._lock:
            self._value += delta

    def decr(self, delta=1):
        '''
        Decrement the counter with locking
        '''
        with SharedCounter._lock:
            self.incr(-delta)