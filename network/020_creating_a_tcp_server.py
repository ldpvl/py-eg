
from socketserver import BaseRequestHandler, TCPServer, StreamRequestHandler


class EchoHandler(BaseRequestHandler):
    def handle(self) -> None:
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)


if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    # serv = ThreadingTCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

# One issue with forking and threaded servers is that they spawn a new process or thread
# on each client connection. There is no upper bound on the number of allowed clients,
# so a malicious hacker could potentially launch a large number of simultaneous con‐
# nections in an effort to make your server explode.

# If this is a concern, you can create a pre-allocated pool of worker threads or processes.
# To do this, you create an instance of a normal nonthreaded server, but then launch the
# serve_forever() method in a pool of multiple threads. For example:
if __name__ == '__main__':
    from threading import Thread

    NWORKERS = 16
    serv = TCPServer(('', 20000), EchoHandler)

    for n in range(NWORKERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()

    serv.serve_forever()


import socket

# The StreamRequestHandler class is actually a bit more
# flexible, and supports some features that can be enabled through the specification of
# additional class variables. For example:
class EchoHandler(StreamRequestHandler):
    # Optional settings (defaults shown)
    timeout = 5  # Timeout on all socket operations
    rbufsize = -1  # Read buffer size
    wbufsize = 0  # Write buffer size
    disable_nagle_algorithm = False  # Sets TCP_NODELAY socket option

    def handle(self):
        print('Got connection from', self.client_address)
        try:
            for line in self.rfile:
                # self.wfile is a file-like object for writing
                self.wfile.write(line)
        except socket.timeout:
            print('Timed out!')


# Finally, it should be noted that most of Python’s higher-level networking modules (e.g.,
# HTTP, XML-RPC, etc.) are built on top of the socketserver functionality. That said,
# it is also not difficult to implement servers directly using the socket library as well. Here
# is a simple example of directly programming a server with Sockets:


# from socket import socket, AF_INET, SOCK_STREAM
#
# def echo_handler(address, client_sock):
#     print('Got connection from {}'.format(address))
#     while True:
#         msg = client_sock.recv(8192)
#         if not msg:
#             break
#         client_sock.sendall(msg)
#     client_sock.close()
#
#
# def echo_server(address, backlog=5):
#     sock = socket(AF_INET, SOCK_STREAM)
#     sock.bind(address)
#     sock.listen(backlog)
#     while True:
#         client_sock, client_addr = sock.accept()
#         echo_handler(client_addr, client_sock)
#
#
# if __name__ == '__main__':
#     echo_server(('', 20000))