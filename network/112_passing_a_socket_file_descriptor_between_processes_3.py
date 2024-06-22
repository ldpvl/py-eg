
import logging
import sys
import os
import tempfile
import struct

from multiprocessing.reduction import recv_handle, send_handle
from multiprocessing.connection import Listener, Client
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SCM_RIGHTS, AF_UNIX, CMSG_LEN, socket
from threading import Thread

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)

# Since this technique is not widely known, here is a
# different implementation of the server that shows how to pass descriptors using sockets:

def send_fd(sock, fd):
    '''
    Send a single file descriptor.
    '''
    sock.sendmsg([b'x'], [(SOL_SOCKET, SCM_RIGHTS, struct.pack('i', fd))])
    ack = sock.recv(2)
    assert ack == b'OK'

def server(work_address, port):
    # Wait for the worker to connect
    work_serv = socket(AF_UNIX, SOCK_STREAM)
    work_serv.bind(work_address)
    work_serv.listen(1)
    worker, addr = work_serv.accept()

    # Now run a TCP/IP server and send clients to worker
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    s.bind(('', port))
    s.listen(1)

    while True:
        client, addr = s.accept()
        logging.info('SERVER: Got connection from', addr)
        send_fd(worker, client.fileno())
        client.close()


# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) != 3:
#         print('Usage: server.py server_address port', file=sys.stderr)
#         raise SystemExit(1)
#     server(sys.argv[1], int(sys.argv[2]))


def recv_fd(sock):
    msg, ancdata, flags, addr = sock.recvmsg(1, CMSG_LEN(struct.calcsize('i')))
    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    assert cmsg_level == SOL_SOCKET and cmsg_type == SCM_RIGHTS
    sock.sendall(b'OK')
    return struct.unpack('i', cmsg_data)[0]


def worker(server_address):
    serv = socket(AF_UNIX, SOCK_STREAM)
    serv.connect(server_address)
    while True:
        fd = recv_fd(serv)
        print('WORKER: GOT FD', fd)
        with socket(AF_INET, SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                print('WORKER: RECV {!r}'.format(msg))
                client.send(msg)


# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) != 2:
#         print('Usage: worker.py server_address', file=sys.stderr)
#         raise SystemExit(1)
#     worker(sys.argv[1])