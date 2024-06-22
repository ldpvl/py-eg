
import requests

r = requests.get('http://httpbin.org/get?name=Dave&n=37',
                 headers = { 'User-agent': 'goaway/1.0' })
resp = r.json()
print(resp['headers'])
print(resp['args'])
print(r.headers)
print(r.text)

resp2 = requests.get('http://httpbin.org/', cookies=resp.cookies)