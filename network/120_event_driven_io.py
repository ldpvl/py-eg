# At a fundamental level, event-driven I/O is a technique that takes basic I/O operations
# (e.g., reads and writes) and converts them into events that must be handled by your
# program. For example, whenever data was received on a socket, it turns into a “receive”
# event that is handled by some sort of callback method or function that you supply to
# respond to it. As a possible starting point, an event-driven framework might start with
# a base class that implements a series of basic event handler methods like this:

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


# The key to the event loop is the select() call, which polls file descriptors for
# activity. Prior to calling select(), the event loop simply queries all of the handlers to
# see which ones want to receive or send. It then supplies the resulting lists to select().
# As a result, select() returns the list of objects that are ready to receive or send. The
# corresponding handle_receive() or handle_send() methods are triggered.

import select


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


import socket
import time
import logging
import sys

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)


class UDPServer(EventHandler):
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):
        logging.info(f'{self.__class__.__qualname__}: returning fileno {self.sock.fileno()}')
        return self.sock.fileno()

    def wants_to_receive(self):
        return True


class UDPTimeServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(1)
        self.sock.sendto(time.ctime().encode('ascii'), addr)


class UDPEchoServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(8192)
        self.sock.sendto(msg, addr)


from threading import Thread


def start_event_loop():
    t = Thread(target=event_loop, kwargs={'handlers': [UDPTimeServer(('', 14000)), UDPEchoServer(('', 15000))]})
    t.daemon = True
    t.start()


start_event_loop()

from socket import *

s = socket(AF_INET, SOCK_DGRAM)
logging.info(f"Send data to UDPTimeServer, response from TimeServer: {s.sendto(b'', ('localhost', 14000))}")
logging.info(f'Received from UDPTimeServer: {s.recvfrom(128)}')
logging.info(f"Sent data to UDPEchoServer, response from TimeServer: {s.sendto(b'Hello', ('localhost', 15000))}")
logging.info(f'Received from UDPEchoServer: {s.recvfrom(128)}')


# Implementing a TCP server is somewhat more complex, since each client involves the
# instantiation of a new handler object

# The key to the TCP example is the addition and removal of clients from the handler list.
# On each connection, a new handler is created for the client and added to the list. When
# the connection is closed, each client must take care to remove themselves from the list.
class TCPServer(EventHandler):
    def __init__(self, address, client_handler, handler_list):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        self.sock.bind(address)
        self.sock.listen(1)
        self.client_handler = client_handler
        self.handler_list = handler_list

    def fileno(self):
        logging.info(f'{self.__class__.__qualname__}: returning fileno {self.sock.fileno()}')
        return self.sock.fileno()

    def wants_to_receive(self):
        return True

    def handle_receive(self):
        client, addr = self.sock.accept()
        # Add the client to the event loop's handler list
        self.handler_list.append(self.client_handler(client, self.handler_list))


class TCPClient(EventHandler):
    def __init__(self, sock, handler_list):
        self.sock = sock
        self.handler_list = handler_list
        self.outgoing = bytearray()

    def fileno(self):
        logging.info(f'{self.__class__.__qualname__}: returning fileno {self.sock.fileno()}')
        return self.sock.fileno()

    def close(self):
        self.sock.close()
        # Remove myself from the event loop's handler list
        self.handler_list.remove(self)

    def wants_to_send(self):
        return True if self.outgoing else False

    def handle_send(self):
        nsent = self.sock.send(self.outgoing)
        self.outgoing = self.outgoing[nsent:]


class TCPEchoClient(TCPClient):
    def wants_to_receive(self):
        return True

    def handle_receive(self):
        data = self.sock.recv(8192)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)


def start_tcp_server_event_loop():
    handlers = []
    handlers.append(TCPServer(('', 16000), TCPEchoClient, handlers))
    t = Thread(target=event_loop, kwargs={'handlers': handlers})
    t.daemon = True
    t.start()


start_tcp_server_event_loop()

s = socket(AF_INET, SOCK_DGRAM)
logging.info(f"Sent data to TCPEchoServer, response from TimeServer: {s.sendto(b'Hello', ('localhost', 15000))}")
logging.info(f'Received from TCPEchoServer: {s.recvfrom(128)}')


# Virtually all event-driven frameworks operate in a manner that is similar to that shown
# in the solution. The actual implementation details and overall software architecture
# might vary greatly, but at the core, there is a polling loop that checks sockets for activity
# and which performs operations in response.

# One potential benefit of event-driven I/O is that it can handle a very large number of
# simultaneous connections without ever using threads or processes. That is, the se
# lect() call (or equivalent) can be used to monitor hundreds or thousands of sockets
# and respond to events occuring on any of them. Events are handled one at a time by the
# event loop, without the need for any other concurrency primitives.

# The downside to event-driven I/O is that there is no true concurrency involved. If any
# of the event handler methods blocks or performs a long-running calculation, it blocks
# the progress of everything. There is also the problem of calling out to library functions
# that aren’t written in an event-driven style. There is always the risk that some library
# call will block, causing the event loop to stall.

# Problems with blocking or long-running calculations can be solved by sending the work
# out to a separate thread or process. However, coordinating threads and processes with
# an event loop is tricky.