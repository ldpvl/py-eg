
import logging
import multiprocessing
import socket
import sys

from multiprocessing.reduction import recv_handle, send_handle

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)

def worker(in_p, out_p):
    out_p.close()
    while True:
        fd = recv_handle(in_p)
        logging.info('CHILD: GOT FD', fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as s:
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                logging.info('CHILD: RECV {!r}'.format(msg))
                s.send(msg)


def server(address, in_p, out_p, worker_pid):
    in_p.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(address)
    s.listen(1)
    while True:
        client, addr = s.accept()
        logging.info('SERVER: Got connection from', addr)
        send_handle(out_p, client.fileno(), worker_pid)
        client.close()


# In this example, two processes are spawned and connected by a multiprocessing Pipe
# object. The server process opens a socket and waits for client connections. The worker
# process merely waits to receive a file descriptor on the pipe using recv_handle(). When
# the server receives a connection, it sends the resulting socket file descriptor to the worker
# using send_handle(). The worker takes over the socket and echoes data back to the
# client until the connection is closed.

if __name__ == '__main__':
    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker, args=(c1,c2))
    worker_p.start()
    logging.info('Started worker process')
    server_p = multiprocessing.Process(target=server,
    args=(('', 15000), c1, c2, worker_p.pid))
    server_p.start()
    logging.info('Started server process')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 15000))
        logging.info('Connected to server')
    c1.close()
    c2.close()