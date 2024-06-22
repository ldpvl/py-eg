# You need to store state that’s specific to the currently executing thread and not visible
# to other threads.

# To do this, create a thread-local storage object using
# threading.local()

from socket import socket, AF_INET, SOCK_STREAM
from functools import partial
import threading

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.local = threading.local()

    def __enter__(self):
        if hasattr(self.local, 'sock'):
            raise RuntimeError('Already connected')
        # The reason it works is that each thread actually creates its own dedicated socket con‐
        # nection (stored as self.local.sock). Thus, when the different threads perform socket
        # operations, they don’t interfere with one another as they are being performed on dif‐
        # ferent sockets.
        self.local.sock = socket(self.family, self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.local.sock.close()
        del self.local.sock


def test(conn):
    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')
        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv, 8192), b''))
    print('Got {} bytes'.format(len(resp)))



if __name__ == '__main__':
    conn = LazyConnection(('www.python.org', 80))
    t1 = threading.Thread(target=test, args=(conn,))
    t2 = threading.Thread(target=test, args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()