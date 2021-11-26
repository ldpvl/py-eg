import json


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


json_string = """\
{
    "firstName": "John",
    "lastName": "Smith",
    "gender": "man",
    "age": 32,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021"
    },
    "phoneNumbers": [
        { "type": "home", "number": "212 555-1234" },
        { "type": "fax", "number": "646 555-4567" }
    ]
}"""

john_smith = json.loads(json_string, object_hook=JSONObject)
print(john_smith.firstName)
print(f'{john_smith.age} {type(john_smith.age)}')
print(john_smith.address.streetAddress)
print(john_smith.phoneNumbers[0].number)
