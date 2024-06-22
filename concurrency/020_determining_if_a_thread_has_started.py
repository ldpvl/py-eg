# Event objects are best used for one-time events. That is, you create an event, threads
# wait for the event to be set, and once set, the Event is discarded. Although it is possible
# to clear an event using its clear() method, safely clearing an event and waiting for it
# to be set again is tricky to coordinate, and can lead to missed events, deadlock, or other
# problems (in particular, you can’t guarantee that a request to clear an event after setting
# it will execute before a released thread cycles back to wait on the event again).


from threading import Thread, Event
import time
import threading

def event_example():
    # Code to execute in an independent thread
    def countdown(n, started_evt):
        print('countdown starting')
        started_evt.set()

        while n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(1)

    # Create the event object that will be used to signal startup
    started_evt = Event()
    # Launch the thread and pass the startup event
    print('Launching countdown',)

    t = Thread(target=countdown, args=(10, started_evt))
    t.start()
    # Wait for the thread to start
    # the event makes the main
    # thread wait until the countdown() function
    # has first printed the startup message
    started_evt.wait()
    print('this message always printed after the countdown start message: countdown is running')



# event_example()


# If a thread is going to repeatedly signal an event over and over, you’re probably better
# off using a Condition object instead.


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        '''
        Run the timer and notify waiting threads after each interval
        '''
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()

    def wait_for_tick(self):
        '''
        Wait for the next tick of the timer
        '''
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


def condition_example():
    ptimer = PeriodicTimer(5)
    ptimer.start()

    # Two threads that synchronize on the timer
    def countdown(nticks):
        while nticks > 0:
            ptimer.wait_for_tick()
            print('T-minus', nticks)
            nticks -= 1

    def countup(last):
        n = 0
        while n < last:
            ptimer.wait_for_tick()
            print('Counting', n)
            n += 1

    threading.Thread(target=countdown, args=(10,)).start()
    threading.Thread(target=countup, args=(5,)).start()


# condition_example()


# A critical feature of Event objects is that they wake all waiting threads. If you are writing
# a program where you only want to wake up a single waiting thread, it is probably better
# to use a Semaphore or Condition object instead.


def semaphore_example():
    # Worker thread
    def worker(n, sema):
        # Wait to be signaled
        sema.acquire()

        # Do some work
        print('Working', n)

    # Create some threads
    sema = threading.Semaphore(0)
    nworkers = 10

    for n in range(nworkers):
        t = threading.Thread(target=worker, args=(n, sema,))
        t.start()

    print('Sleeping for a few seconds')
    time.sleep(5)
    sema.release()

    print('Sleeping for a few seconds')
    time.sleep(5)
    sema.release()


semaphore_example()