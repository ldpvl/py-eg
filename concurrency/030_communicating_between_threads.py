
# from queue import Queue
# from threading import Thread
#
# # A thread that produces data
# def producer(out_q):
#     while True:
#         # Produce some data
#         ...
#         out_q.put(data)
#
#
# # A thread that consumes data
# def consumer(in_q):
#     while True:
#         # Get some data
#         data = in_q.get()
#         # Process the data
#         ...
#
#
# # Create the shared queue and launch both threads
# q = Queue()
# t1 = Thread(target=consumer, args=(q,))
# t2 = Thread(target=producer, args=(q,))
# t1.start()
# t2.start()


# Queue instances already have all of the required locking, so they can be safely shared by
# as many threads as you wish.
# When using queues, it can be somewhat tricky to coordinate the shutdown of the pro‐
# ducer and consumer. A common solution to this problem is to rely on a special sentinel
# value, which when placed in the queue, causes consumers to terminate. For example:


# from queue import Queue
# from threading import Thread
#
# # Object that signals shutdown
# _sentinel = object()
#
# # A thread that produces data
# def producer(out_q):
#     while running:
#         # Produce some data
#         ...
#         out_q.put(data)
#
#     # Put the sentinel on the queue to indicate completion
#     out_q.put(_sentinel)
#
#
# # A thread that consumes data
# def consumer(in_q):
#     while True:
#         # Get some data
#         data = in_q.get()
#
#         # Check for termination
#         if data is _sentinel:
#             # A subtle feature of this example is that the consumer, upon receiving the special sentinel
#             # value, immediately places it back onto the queue. This propagates the sentinel to other
#             # consumers threads that might be listening on the same queue—thus shutting them all
#             # down one after the other.
#             in_q.put(_sentinel)
#             break
#
#         # Process the data
#         ...