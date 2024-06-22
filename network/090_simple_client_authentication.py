
import hmac
import os
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


# The general idea is that upon connection, the server presents the client with a message
# of random bytes (returned by os.urandom(), in this case). The client and server both
# compute a cryptographic hash of the random data using hmac and a secret key known
# only to both ends. The client sends its computed digest back to the server, where it is
# compared and used to decide whether to accept or reject the connection.

# Comparison of resulting digests should be performed using the hmac.compare_di
# gest() function. This function has been written in a way that avoids timing-analysis-
# based attacks and should be used instead of a normal comparison operator (==).

def client_authenticate(connection, secret_key):
    '''
    Authenticate client to a remote service.
    connection represents a network connection.
    secret_key is a key known only to both client/server.
    '''

    message = connection.recv(32)
    logging.info(f'Client authentication: received authentication message')
    # A common use of hmac authentication is in internal messaging systems and interprocess
    # communication. For example, if you are writing a system that involves multiple pro‐
    # cesses communicating across a cluster of machines, you can use this approach to make
    # sure that only allowed processes are allowed to connect to one another. In fact, HMAC-
    # based authentication is used internally by the multiprocessing library when it sets up
    # communication with subprocesses

    # It’s important to stress that authenticating a connection is not the same as encryption.
    # Subsequent communication on an authenticated connection is sent in the clear, and
    # would be visible to anyone inclined to sniff the traffic (although the secret key known
    # to both sides is never transmitted).

    hash = hmac.new(secret_key, message, digestmod='sha1')
    digest = hash.digest()

    logging.info(f'Client authentication: created hash value of message using the secret key. Sending this to the server...')

    connection.send(digest)


def server_authenticate(connection, secret_key):
    '''
    Request client authentication.
    '''
    size = 32
    message = os.urandom(size) # a bytes object containing random bytes suitable for cryptographic use.
    logging.info(f'Server authentication: created a random {size} bytes message. Sending this to the client...')
    connection.send(message)
    logging.info(f'Server authentication: message sent')

    logging.info(f'Server authentication: encrypting the random message using the shared secret key')
    hash = hmac.new(secret_key, message, digestmod='sha1')
    digest = hash.digest()

    logging.info(f'Server authentication: asking the client for the encrypted message using the shared secret key for comparison')
    response = connection.recv(len(digest))
    logging.info(f'Server authentication: received the encrypted message from the client, going to perform comparison')

    comparison_result = hmac.compare_digest(digest, response)
    logging.info(f'Server authentication: comparison is successful: {comparison_result}')
    return comparison_result


from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'peekaboo'

def echo_handler(client_sock):
    if not server_authenticate(client_sock, secret_key):
        logging.info(f'Server handler: authentication failed, closing connection')
        client_sock.close()
        return

    while True:
        msg = client_sock.recv(8192)
        logging.info(f'Server handler: received message from client "{msg.decode()}"')
        if not msg:
            logging.warning('Server handler: empty message received from client')
            break
        logging.info(f'Server handler: sending ack back to client')
        client_sock.sendall(f'Server handler - ack: received following message from client "{msg.decode()}"'.encode())


def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    logging.info(f'Server: started at {address}')
    while True:
        logging.info('Server: about to do s.accept() to wait for an incoming connection. Return a new socket '
              'representing the connection, and the address of the client.')
        c, a = s.accept()
        logging.info('Server: received an incoming connection from client, passing connection to the handler')
        echo_handler(c)


from threading import Thread


# Run the server
def start_echo_server():
    t = Thread(target=echo_server, args=(('', 18000),))
    t.daemon = True
    t.start()


start_echo_server()



def start_client():
    # run client
    s = socket(AF_INET, SOCK_STREAM)

    address = ('localhost', 18000)
    logging.info(f'Client connecting to {address}')
    s.connect(address)
    logging.info(f'Client connected to {address}')
    return s


s = start_client()
client_authenticate(s, secret_key)

logging.info('Client: sending message to server')
s.send(b'Hello World')
logging.info(f'Response from server: {s.recv(1024).decode()}')
logging.info('Client: sending message to server')
s.send(b'Foo bar')
logging.info(f'Response from server: {s.recv(1024).decode()}')

s.close()
s = start_client()

logging.info(f'Trying a bad secret key...')
client_authenticate(s, b'bad')
