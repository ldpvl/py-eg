
from multiprocessing import freeze_support
freeze_support()
import time



def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]

def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]


from multiprocessing import Process

def start_server():
    from socket import AF_INET, SOCK_STREAM, socket
    import numpy
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 25000))
    s.listen(1)
    c, a = s.accept()

    # wait for client to connect
    time.sleep(2)
    print(f'Server: sending stuff', flush=True)
    a = numpy.arange(0.0, 50000000.0)
    send_from(a, c)




def start_server_process():
    print(f'Starting server', flush=True)
    p = Process(target=start_server)
    p.start()
    print(f'Server started')





def start_client():
    import numpy
    from socket import AF_INET, SOCK_STREAM, socket
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('localhost', 25000))
    print('Client connected', flush=True)
    a = numpy.zeros(shape=50000000, dtype=float)
    recv_into(a, c)
    print(f'{a[0:10]}', flush=True)


def start_client_process():
    print(f'Starting client', flush=True)
    p = Process(target=start_client)
    p.start()
    print(f'Client started', flush=True)


# need to fork
start_server_process()
time.sleep(10)
start_client_process()
time.sleep(10)