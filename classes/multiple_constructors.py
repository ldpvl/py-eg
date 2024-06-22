# When defining a class with multiple constructors, you should make the __init__()
# function as simple as possible—doing nothing more than assigning attributes from
# given values. Alternate constructors can then choose to perform advanced operations
# if needed.

import time

class Date:
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        # Alternate constructor

    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

a = Date(2012, 12, 21) # Primary
b = Date.today() # Alternate