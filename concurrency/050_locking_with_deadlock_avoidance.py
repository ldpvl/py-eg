# You’re writing a multithreaded program where threads need to acquire more than one
# lock at a time while avoiding deadlock.

# In multithreaded programs, a common source of deadlock is due to threads that attempt
# to acquire multiple locks at once. For instance, if a thread acquires the first lock, but
# then blocks trying to acquire the second lock, that thread can potentially block the
# progress of other threads and make the program freeze.

# One solution to deadlock avoidance is to assign each lock in the program a unique
# number, and to enforce an ordering rule that only allows multiple locks to be acquired
# in ascending order. This is surprisingly easy to implement using a context manager as
# follows:


import threading
import logging
import sys
import traceback

from time import sleep
from contextlib import contextmanager

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)

# Thread-local state to store information on locks already acquired
_local = threading.local()

@contextmanager
def acquire(*locks):
    # By sorting the locks, they always get acquired in a consistent order regardless
    # of how the user might have provided them to acquire()
    locks = sorted(locks, key=lambda x: id(x))
    logging.info(f'IDs of locks to be acquired after sorting: {[id(_) for _ in locks]}')

    # Make sure lock order of previously acquired locks is not violated
    # The solution uses thread-local storage to solve a subtle problem with detecting potential
    # deadlock if multiple acquire() operations are nested.
    acquired = getattr(_local, 'acquired', [])
    logging.info(f'Previously acquired lock ids: {[id(_) for _ in acquired]}')


    if acquired:
        max_lock_id = max(id(lock) for lock in acquired)
        if max(id(lock) for lock in acquired) >= id(locks[0]):
            # This crash is caused by the fact that each thread remembers the locks it has already
            # acquired. The acquire() function checks the list of previously acquired locks and en‐
            # forces the ordering constraint that previously acquired locks must have an object ID
            # that is less than the new locks being acquired.
            raise RuntimeError(f'Lock Order Violation: ID of max acquired lock {max_lock_id} >= {id(locks[0])}')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
            logging.info(f'Acquired lock {id(lock)}')
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
            logging.info(f'Released lock {id(lock)}')
        del acquired[-len(locks):]



def test():
    import threading
    x_lock = threading.Lock()
    y_lock = threading.Lock()

    def thread_1():
        while True:
            with acquire(x_lock, y_lock):
                logging.info('Thread-1')
                sleep(1)

    def thread_2():
        while True:
            with acquire(y_lock, x_lock):
                logging.info('Thread-2')
                sleep(1.5)

    t1 = threading.Thread(target=thread_1)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=thread_2)
    t2.daemon = True
    t2.start()


    sleep(5)




def test_violation():
    import threading
    x_lock = threading.Lock()
    y_lock = threading.Lock()

    def thread_1():
        while True:
            with acquire(x_lock):
                with acquire(y_lock):
                    logging.info('Thread-1')
                    sleep(1)

    def thread_2():
        while True:
            with acquire(y_lock):
                with acquire(x_lock):
                    logging.info('Thread-2')
                    sleep(1.5)

    t1 = threading.Thread(target=thread_1)
    t1.daemon = True
    t1.start()
    t2 = threading.Thread(target=thread_2)
    t2.daemon = True
    t2.start()

    sleep(5)



def main():
    # test()
    test_violation()


if __name__ == "__main__":
    main()