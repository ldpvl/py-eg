# Thread communication with a queue is a one-way and nondeterministic process. In
# general, there is no way to know when the receiving thread has actually received a
# message and worked on it. However, Queue objects do provide some basic completion
# features, as illustrated by the task_done() and join() methods in this example:

# from queue import Queue
# from threading import Thread
#
# # A thread that produces data
# def producer(out_q):
#     while running:
#         # Produce some data
#         ...
#         out_q.put(data)
#
# # A thread that consumes data
# def consumer(in_q):
#     while True:
#         # Get some data
#         data = in_q.get()
#         # Process the data
#         ...
#         # Indicate completion
#         # Once the task is done it calls in_q.task_done() which increments the internal counter of the number
#         # of completed tasks. And with q.join() the main thread will wait for the internal counter to reach
#         # the number of items put in the queue, indicating all the items are processed.
#         in_q.task_done()
#
# # Create the shared queue and launch both threads
# q = Queue()
# t1 = Thread(target=consumer, args=(q,))
# t2 = Thread(target=producer, args=(q,))
# t1.start()
# t2.start()
#
# # Wait for all produced items to be consumed
# q.join()

# If a thread needs to know immediately when a consumer thread has processed a par‐
# ticular item of data, you should pair the sent data with an Event object that allows the
# producer to monitor its progress. For example:

# from queue import Queue
# from threading import Thread, Event
#
# # A thread that produces data
# def producer(out_q):
#     while running:
#         # Produce some data
#         ...
#         # Make an (data, event) pair and hand it to the consumer
#         evt = Event()
#         out_q.put((data, evt))
#         ...
#         # Wait for the consumer to process the item
#         evt.wait()
#
# # A thread that consumes data
# def consumer(in_q):
#     while True:
#         # Get some data
#         data, evt = in_q.get()
#         # Process the data
#         ...
#         # Indicate completion
#         evt.set()