
import cgi

def notfound_404(environ, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Not Found']

class PathDispatcher:
    def __init__(self):
        self.pathmap = {}

    def __call__(self, environ, start_response):
        # The environ argument is a dictionary that contains values inspired by the CGI interface
        # provided by various web servers such as Apache
        # https://datatracker.ietf.org/doc/html/rfc3875#section-4.1

        # The start_response argument is a function that must be called to initiate a response.
        # The first argument is the resulting HTTP status. The second argument is a list of (name,
        # value) tuples that make up the HTTP headers of the response.
        path = environ['PATH_INFO']

        # The call to cgi.FieldStorage() extracts supplied query parameters
        # from the request and puts them into a dictionary-like object for later use.
        params = cgi.FieldStorage(environ['wsgi.input'],
                                  environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        handler = self.pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function


import time

_hello_resp = '''\
<html>
    <head>
        <title>Hello {name}</title>
    </head>
    <body>
        <h1>Hello {name}!</h1>
    </body>
</html>'''


def hello_world(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8') # byte strings must be used in the result


# Although WSGI applications are commonly defined as a function, as shown, an instance
# may also be used as long as it implements a suitable __call__() method. For example:

# class WSGIApplication:
#     def __init__(self):
#         ...
#     def __call__(self, environ, start_response)
#         ...


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()


# u = urlopen('http://localhost:8080/hello?name=Guido')
# print(u.read().decode('utf-8'))