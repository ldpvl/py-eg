
import pickle

class RPCHandler:
    def __init__(self):
        self._functions = {}

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass


from multiprocessing.connection import Listener
from threading import Thread


def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client,))
        t.daemon = True
        t.start()


# Some remote functions
def add(x, y):
    return x + y

def sub(x, y):
    return x - y


# Register with a handler
handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)


import pickle

# RPC proxy class that forwards requests
class RPCProxy:
    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result
        return do_rpc


# Run the server
def start_rpc_server():
    #rpc_server(handler, ('localhost', 17000), authkey=b'peekaboo')
    t = Thread(target=rpc_server, args=(handler, ('localhost', 17000), b'peekaboo'))
    t.daemon = True
    t.start()


start_rpc_server()

from multiprocessing.connection import Client
c = Client(('localhost', 17000), authkey=b'peekaboo')
proxy = RPCProxy(c)
print(proxy.add(2, 3))
print(proxy.sub(2, 3))
print(proxy.sub([1, 2], 3))

# It should be noted that many messaging layers (such as multiprocessing) already se‐
# rialize data using pickle. If this is the case, the pickle.dumps() and pickle.loads()
# calls can be eliminated.
