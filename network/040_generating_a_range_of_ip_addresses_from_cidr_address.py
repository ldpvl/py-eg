
import ipaddress
from pprint import pprint

net = ipaddress.ip_network('123.45.67.64/27')
print(net)
pprint(list(net))
print(net.num_addresses)
print(net[2])

net6 = ipaddress.ip_network('12:3456:78:90ab:cd:ef01:23:30/125')
pprint(list(net6))
