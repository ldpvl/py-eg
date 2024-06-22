# Due to a global interpreter lock (GIL), Python threads are restricted to an execution
# model that only allows one thread to execute in the interpreter at any given time. For
# this reason, Python threads should generally not be used for computationally intensive
# tasks where you are trying to achieve parallelism on multiple CPUs. They are much
# better suited for I/O handling and handling concurrent execution in code that performs
# blocking operations (e.g., waiting for I/O, waiting for results from a database, etc.).

import time

def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)

from threading import Thread
t = Thread(target=countdown, args=(3,))
t.start()
# t.join() # wait for the thread to terminate

if t.is_alive():
    print('Still running')
else:
    print('Completed')

# The interpreter remains running until all threads terminate. For long-running threads
# or background tasks that run forever, you should consider making the thread daemonic.

# For example:
# t = Thread(target=countdown, args=(10,), daemon=True)
# t.start()

# Daemonic threads can’t be joined. However, they are destroyed automatically when the
# main thread terminates.

# Beyond the two operations shown, there aren’t many other things you can do with
# threads. For example, there are no operations to terminate a thread, signal a thread,
# adjust its scheduling, or perform any other high-level operations. If you want these
# features, you need to build them yourself.

# If you want to be able to terminate threads, the thread must be programmed to poll for
# exit at selected points. For example, you might put your thread in a class such as this:

class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        print('Terminating')
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(1)


c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
c.terminate()
t.join()
print(f'Thread {t} terminated')

# Sometimes you will see threads defined via inheritance from the Thread class. For
# example:

# from threading import Thread
# class CountdownThread(Thread):
#     def __init__(self, n):

# Although this works, it introduces an extra dependency between the code and the
# threading library. That is, you can only use the resulting code in the context of threads,
# whereas the technique shown earlier involves writing code with no explicit dependency
# on threading. By freeing your code of such dependencies, it becomes usable in other
# contexts that may or may not involve threads. For instance, you might be able to execute
# your code in a separate process using the multiprocessing module using code like this:

# import multiprocessing
# c = CountdownTask(5)
# p = multiprocessing.Process(target=c.run)
# p.start()