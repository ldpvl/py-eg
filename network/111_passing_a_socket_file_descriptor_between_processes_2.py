
import logging
import sys
import os
import tempfile

from multiprocessing.reduction import recv_handle, send_handle
from multiprocessing.connection import Listener, Client
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)

# Passing file descriptors between processes is something that many programmers don’t
# even realize is possible. However, it can sometimes be a useful tool in building scalable
# systems. For example, on a multicore machine, you could have multiple instances of the
# Python interpreter and use file descriptor passing to more evenly balance the number
# of clients being handled by each interpreter.
# The send_handle() and recv_handle() functions shown in the solution really only
# work with multiprocessing connections. Instead of using a pipe, you can connect in‐
# terpreters as shown in Recipe 11.7, and it will work as long as you use UNIX domain
# sockets or Windows pipes. For example, you could implement the server and worker
# as completely separate programs to be started separately. Here is the implementation of
# the server:

def server(work_address, port):
    # Wait for the worker to connect
    work_serv = Listener(work_address, authkey=b'peekaboo')
    worker = work_serv.accept()
    worker_pid = worker.recv()

    # Now run a TCP/IP server and send clients to worker
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    s.bind(('', port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        logging.info('SERVER: Got connection from', addr)
        send_handle(worker, client.fileno(), worker_pid)
        client.close()

# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) != 3:
#         print('Usage: server.py server_address port', file=sys.stderr)
#         raise SystemExit(1)
#     server(sys.argv[1], int(sys.argv[2]))


def worker(server_address):
    serv = Client(server_address, authkey=b'peekaboo')
    serv.send(os.getpid())
    while True:
        fd = recv_handle(serv)
        logging.info('WORKER: GOT FD', fd)

        with socket(AF_INET, SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                logging.info('WORKER: RECV {!r}'.format(msg))
                client.send(msg)

# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) != 2:
#         print('Usage: worker.py server_address', file=sys.stderr)
#         raise SystemExit(1)
#     worker(sys.argv[1])


servconn = tempfile.mktemp()
server_port = 16500

def start_server():
    t = Thread(target=server, args=(servconn, server_port))
    t.daemon = True
    t.start()


def start_worker():
    t = Thread(target=worker, args=(servconn,))
    t.daemon = True
    t.start()


start_server()
# start_worker()
