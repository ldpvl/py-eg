
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


import ssl

# Generate CA certificate using this command:
# openssl req -newkey rsa:4096 -keyform PEM -keyout ca.key -x509 -days 3650 -outform PEM -out ca.cer

# Generate server certificate and private key
# 1. Generate a server private key:
#    openssl genrsa -out server.key 4096
# 2. Use the server private key to generate a certificate generation request:
#    openssl req -new -key server.key -out server.req -sha256
# 3. Use the certificate generation request and the CA cert to generate the server cert:
#    openssl x509 -req -in server.req -CA ca.cer -CAkey ca.key -set_serial 100 -extensions server -days 1460 -outform PEM -out server.cer -sha256
# 4. Clean up – now that the cert has been created, we no longer need the request:
#    rm server.req

KEYFILE = os.path.join(current_dir, 'resources/server.key') # Private key of the server
CERTFILE = os.path.join(current_dir, 'resources/server.cer') # The server certificate (given to client)
# The certificate file contains the public key and is pre‐
# sented to the remote peer on each connection. For public servers, certificates are nor‐
# mally signed by a certificate authority such as Verisign, Equifax, or similar organization
# (something that costs money). To verify server certificates, clients maintain a file con‐
# taining the certificates of trusted certificate authorities. For example, web browsers
# maintain certificates corresponding to the major certificate authorities and use them to
# verify the integrity of certificates presented by web servers during HTTPS connections.

# Generate client certificate and private key
# 1. Generate a private key for the SSL client:
#    openssl genrsa -out client.key 4096
# 2. Use the client’s private key to generate a cert request:
#    openssl req -new -key client.key -out client.req
# 3. Issue the client certificate using the cert request and the CA cert/key:
#    openssl x509 -req -in client.req -CA ca.cer -CAkey ca.key -set_serial 101 -extensions client -days 365 -outform PEM -out client.cer
# 4. Clean up:
#    rm client.req
CLIENT_KEYFILE = os.path.join(current_dir, 'resources/client.key') # Private key of the server
CLIENT_CERT = os.path.join(current_dir, 'resources/client.cer') # The self-signed server certificate (given to client)
CA_CERT = os.path.join(current_dir, 'resources/ca.cer') # The self-signed server certificate (given to client)


class SSLMixin:
    '''
    Mixin class that adds support for SSL to existing servers based
    on the socketserver module.
    '''

    def __init__(self, *args,
                 keyfile=None,
                 certfile=None,
                 ca_certs=None,
                 cert_reqs=ssl.CERT_NONE,
                 **kwargs):
        self._keyfile = keyfile
        self._certfile = certfile
        self._ca_certs = ca_certs
        self._cert_reqs = cert_reqs
        super().__init__(*args, **kwargs)

    def get_request(self):
        client, addr = super().get_request()
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_verify_locations(cafile=self._ca_certs)
        context.load_cert_chain(certfile=self._certfile, keyfile=self._keyfile)
        with context.wrap_socket(sock=client, server_side=True) as ssl_client:
            return ssl_client, addr
        # client, addr = super().get_request()
        # client_ssl = ssl.wrap_socket(client,
        #                              keyfile=self._keyfile,
        #                              certfile=self._certfile,
        #                              ca_certs=self._ca_certs,
        #                              cert_reqs=self._cert_reqs,
        #                              server_side=True)
        # return client_ssl, addr


# XML-RPC server with SSL
from xmlrpc.server import SimpleXMLRPCServer

class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
    pass


class KeyValueServer:
    _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']

    def __init__(self, *args, **kwargs):
        self._data = {}
        self._serv = SSLSimpleXMLRPCServer(*args, allow_none=True, **kwargs)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value

    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._serv.serve_forever()


from xmlrpc.client import ServerProxy, SafeTransport


class VerifyCertSafeTransport(SafeTransport):
    def __init__(self, cafile, certfile=None, keyfile=None):
        SafeTransport.__init__(self)
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self._ssl_context.load_verify_locations(cafile)
        if certfile:
            self._ssl_context.load_cert_chain(certfile, keyfile)
        self._ssl_context.verify_mode = ssl.CERT_REQUIRED

    def make_connection(self, host):
        # Items in the passed dictionary are passed as keyword
        # arguments to the http.client.HTTPSConnection() constructor.
        # The context argument allows an ssl.SSLContext instance to
        # be passed with information about the SSL configuration
        s = super().make_connection(host)
        return s


def rpc_server():
    kvserv = KeyValueServer(('', 15000),
                            keyfile=KEYFILE,
                            certfile=CERTFILE,
                            ca_certs=CA_CERT,
                            cert_reqs=ssl.CERT_REQUIRED)
    kvserv.serve_forever()


def start_rpc_server_thread():
    t = Thread(target=rpc_server)
    t.daemon = True
    t.start()


start_rpc_server_thread()


# Create client proxy
s = ServerProxy('https://localhost:15000',
                transport=VerifyCertSafeTransport(cafile=CA_CERT,
                                                  certfile=CLIENT_CERT,
                                                  keyfile=CLIENT_KEYFILE),
                allow_none=True)

s.set('foo','bar')
s.set('spam', [1, 2, 3])
print(s.keys())
