# As a rule of thumb, as
# long as you can ensure that threads can hold only one lock at a time, your program will
# be deadlock free. However, once multiple locks are being acquired at the same time, all
# bets are off.

# Detecting and recovering from deadlock is an extremely tricky problem with few elegant
# solutions. For example, a common deadlock detection and recovery scheme involves
# the use of a watchdog timer. As threads run, they periodically reset the timer, and as
# long as everything is running smoothly, all is well. However, if the program deadlocks,
# the watchdog timer will eventually expire. At that point, the program “recovers” by
# killing and then restarting itself.

# Deadlock avoidance is a different strategy where locking operations are carried out in
# a manner that simply does not allow the program to enter a deadlocked state. The
# solution in which locks are always acquired in strict order of ascending object ID can
# be mathematically proven to avoid deadlock, although the proof is left as an exercise to
# the reader (the gist of it is that by acquiring locks in a purely increasing order, you can’t
# get cyclic locking dependencies, which are a necessary condition for deadlock to occur).

# As a final example, a classic thread deadlock problem is the so-called “dining philoso‐
# pher’s problem.” In this problem, five philosophers sit around a table on which there
# are five bowls of rice and five chopsticks. Each philosopher represents an independent
# thread and each chopstick represents a lock. In the problem, philosophers either sit and
# think or they eat rice. However, in order to eat rice, a philosopher needs two chopsticks.
# Unfortunately, if all of the philosophers reach over and grab the chopstick to their left,
# they’ll all just sit there with one stick and eventually starve to death. It’s a gruesome
# scene.

# Using the solution, here is a simple deadlock free implementation of the dining philos‐
# opher’s problem:

deadlock_avoidance = __import__('050_locking_with_deadlock_avoidance')

import threading

from time import sleep
from random import randint

# The philosopher thread
def philosopher(left, right):
    while True:
        with deadlock_avoidance.acquire(left, right):
            deadlock_avoidance.logging.info(f'{threading.current_thread()} eating')
        sleep(randint(0, 1))

# The chopsticks (represented by locks)
NSTICKS = 5
chopsticks = [threading.Lock() for n in range(NSTICKS)]

# Create all of the philosophers
for n in range(NSTICKS):
    t = threading.Thread(target=philosopher,
                         # (n+1) % NSTICKS follows the loop of the range(NSTICKS)
                         # 0 => 1, 1 => 2, ... 4 => 0
                         args=(chopsticks[n], chopsticks[(n+1) % NSTICKS]))
    t.start()


