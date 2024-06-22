
import logging
import sys
import os
from threading import Thread

FORMAT = '%(asctime)s %(name)s %(levelname)s %(threadName)s: %(message)s'


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
root.addHandler(handler)

# The ssl module provides support for adding SSL to low-level socket connections. In
# particular, the ssl.wrap_socket() function takes an existing socket and wraps an SSL
# layer around it.


current_dir = os.path.dirname(os.path.abspath(__file__))


from socket import socket, AF_INET, SOCK_STREAM
import ssl

# the pem files were created using: openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem

KEYFILE = os.path.join(current_dir, 'resources/server.key') # Private key of the server

CERTFILE = os.path.join(current_dir, 'resources/server.cer') # The server certificate (given to client)
# The certificate file contains the public key and is pre‐
# sented to the remote peer on each connection. For public servers, certificates are nor‐
# mally signed by a certificate authority such as Verisign, Equifax, or similar organization
# (something that costs money). To verify server certificates, clients maintain a file con‐
# taining the certificates of trusted certificate authorities. For example, web browsers
# maintain certificates corresponding to the major certificate authorities and use them to
# verify the integrity of certificates presented by web servers during HTTPS connections.



def echo_client(s):
    while True:
        data = s.recv(8192)
        if data == b'':
            break
        s.send(data)
    s.close()
    logging.info('Connection closed')

def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)
    # Wrap with an SSL layer requiring client certs
    s_ssl = ssl.wrap_socket(s,
                            keyfile=KEYFILE,
                            certfile=CERTFILE,
                            server_side=True
                            )
    # Wait for connections
    while True:
        try:
            c, a = s_ssl.accept()
            logging.info('Got connection', c, a)
            echo_client(c)
        except Exception as e:
            logging.info(f'{e.__class__}: {e}')


# Run the server
def start_echo_server():
    t = Thread(target=echo_server, args=(('', 20000),))
    t.daemon = True
    t.start()


start_echo_server()



# Start the client
def start_client():
    s = socket(AF_INET, SOCK_STREAM)
    s_ssl = ssl.wrap_socket(s,
                            cert_reqs=ssl.CERT_REQUIRED,
                            ca_certs=CERTFILE)
    s_ssl.connect(('localhost', 20000))
    return s_ssl


s_ssl = start_client()
logging.info(f'Client: sending message to server: {s_ssl.send(b"Hello World?")}')
logging.info(f'Client: received message from server: {s_ssl.recv(8192).decode()}')
