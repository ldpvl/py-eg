# As a general rule, you probably shouldn’t expose an XML-RPC service to the rest of the
# world as a public API. It often works best on internal networks where you might want
# to write simple distributed programs involving a few different machines.

# A downside to XML-RPC is its performance. The SimpleXMLRPCServer implementa‐
# tion is only single threaded, and wouldn’t be appropriate for scaling a large application,
# although it can be made to run multithreaded, as shown in Recipe 11.2. Also, since
# XML-RPC serializes all data as XML, it’s inherently slower than other approaches.

# However, one benefit of this encoding is that it’s understood by a variety of other pro‐
# gramming languages. By using it, clients written in languages other than Python will be
# able to access your service.
# Despite its limitations, XML-RPC is worth knowing about if you ever have the need to
# make a quick and dirty remote procedure call system. Oftentimes, the simple solution
# is good enough.

from xmlrpc.server import SimpleXMLRPCServer

class KeyValueServer:
    _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']

    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
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

# Example
if __name__ == '__main__':
    kvserv = KeyValueServer(('', 15000))
    kvserv.serve_forever()

# >>> from xmlrpc.client import ServerProxy
# >>> s = ServerProxy('http://localhost:15000', allow_none=True)
# >>> s.set('foo', 'bar')
# >>> s.set('spam', [1, 2, 3])
# >>> s.keys()
# ['spam', 'foo']
# >>> s.get('foo')
# 'bar'
# >>> s.get('spam')
# [1, 2, 3]
# >>> s.delete('spam')
# >>> s.exists('spam')
# False
# >>>


# Functions exposed via XML-RPC only work with certain kinds of data such as strings,
# numbers, lists, and dictionaries. For everything else, some study is required. For in‐
# stance, if you pass an instance through XML-RPC, only its instance dictionary is
# handled:

# >>> class Point:
# ... def __init__(self, x, y):
# ... self.x = x
# ... self.y = y
# ...
# >>> p = Point(2, 3)
# >>> s.set('foo', p)
# >>> s.get('foo')
# {'x': 2, 'y': 3}
# >>>

# Similarly, handling of binary data is a bit different than you expect:
# >>> s.set('foo', b'Hello World')
# >>> s.get('foo')
# <xmlrpc.client.Binary object at 0x10131d410>
# >>> _.data
# b'Hello World'
# >>>