
import socket
import os
import logging
import sys
import select

from threading import Thread

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)


from concurrent.futures import ThreadPoolExecutor

class EventHandler:
    def fileno(self):
        'Return the associated file descriptor'
        raise NotImplemented('must implement')

    def wants_to_receive(self):
        'Return True if receiving is allowed'
        return False

    def handle_receive(self):
        'Perform the receive operation'
        pass

    def wants_to_send(self):
        'Return True if sending is requested'
        return False

    def handle_send(self):
        'Send outgoing data'
        pass

class UDPServer(EventHandler):
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):
        logging.info(f'{self.__class__.__qualname__}: returning fileno {self.sock.fileno()}')
        return self.sock.fileno()

    def wants_to_receive(self):
        return True


def event_loop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        # Wait until one or more file descriptors are ready for some kind of I/O.
        # The first three arguments are iterables of file descriptors to be waited for:
        # rlist -- wait until ready for reading
        # wlist -- wait until ready for writing
        can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
        for h in can_recv:
            h.handle_receive()
        for h in can_send:
            h.handle_send()

# In this code, the run() method is used to submit work to the pool along with a callback
# function that should be triggered upon completion. The actual work is then submitted
# to a ThreadPoolExecutor instance. However, a really tricky problem concerns the co‐
# ordination of the computed result and the event loop. To do this, a pair of sockets are
# created under the covers and used as a kind of signaling mechanism. When work is
# completed by the thread pool, it executes the _complete() method in the class. This
# method queues up the pending callback and result before writing a byte of data on one
# of these sockets. The fileno() method is programmed to return the other socket. Thus,
# when this byte is written, it will signal to the event loop that something has happened.
# The handle_receive() method, when triggered, will then execute all of the callback
# functions for previously submitted work.

class ThreadPoolHandler(EventHandler):
    def __init__(self, nworkers):
        if os.name == 'posix':
            self.signal_done_sock, self.done_sock = socket.socketpair()
        else:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            self.signal_done_sock = socket.socket(socket.AF_INET,
                                                  socket.SOCK_STREAM)
            self.signal_done_sock.connect(server.getsockname())
            self.done_sock, _ = server.accept()
            server.close()

        self.pending = []
        self.pool = ThreadPoolExecutor(nworkers)

    def fileno(self):
        return self.done_sock.fileno()

    # Callback that executes when the thread is done
    def _complete(self, callback, r):
        self.pending.append((callback, r.result()))
        logging.info(f'Sending done mesage')
        self.signal_done_sock.send(b'thread is done')

    # Run a function in a thread pool
    def run(self, func, args=(), kwargs={}, *, callback):
        logging.info(f'Sending function to pool: {func.__qualname__} with arguments {args} {kwargs}')
        r = self.pool.submit(func, *args, **kwargs)
        r.add_done_callback(lambda r: self._complete(callback, r))

    def wants_to_receive(self):
        return True

    # Run callback functions of completed work
    def handle_receive(self):
        # Invoke all pending callback functions
        for callback, result in self.pending:
            callback(result)
        self.done_sock.recv(1)
        self.pending = []


pool = ThreadPoolHandler(16)

from time import sleep

def fib(n):
    logging.info(f'Sleep {n} seconds')
    sleep(n)
    # if n < 2:
    #     return 1
    # else:
    #     return fib(n - 1) + fib(n - 2)


class UDPFibServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(128)
        n = int(msg)
        pool.run(fib, (n,), callback=lambda r: self.respond(r, addr))

    def respond(self, result, addr):
        self.sock.sendto(str(result).encode('ascii'), addr)



def start_fib_server_event_loop():
    handlers = [ pool, UDPFibServer(('',16000))]
    t = Thread(target=event_loop, kwargs={'handlers': handlers})
    t.daemon = True
    t.start()
    logging.info(f'Started fib event loop thread')


start_fib_server_event_loop()


from socket import *
sock = socket(AF_INET, SOCK_DGRAM)
for x in range(40):
    logging.info(f'Sending request to calculate fib({x})')
    sock.sendto(str(x).encode('ascii'), ('localhost', 16000))
    resp = sock.recvfrom(8192)
    logging.info(f'fib({x}) = {resp[0].decode()}')