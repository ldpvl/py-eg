
# Although queues are the most common thread communication mechanism, you can
# build your own data structures as long as you add the required locking and synchroni‐
# zation. The most common way to do this is to wrap your data structures with a condition
# variable. For example, here is how you might build a thread-safe priority queue:

import heapq
import threading

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()

    def put(self, item, priority):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]

# The heapq.heappush() function is a built-in function in the Python heapq module.
# It is used to push an element onto a heap, maintaining the heap invariant.
# A heap is a specific kind of data structure in which the element with the lowest value is always the first element.
# This function takes two arguments: the first is the list representing the heap, and the second is the element to be added to the heap.
# The element is added to the end of the list and then "bubbled up" to its correct position in the heap,
# which is determined by the relative ordering of its value to the values of its parent and children nodes.
#
# Here is an example of how you might use the heapq.heappush() function:

# import heapq
#
# heap = []
# heapq.heappush(heap, 5)
# heapq.heappush(heap, 2)
# heapq.heappush(heap, 3)
# heapq.heappush(heap, 1)
#
# print(heap)
# # Output: [1, 2, 3, 5]
