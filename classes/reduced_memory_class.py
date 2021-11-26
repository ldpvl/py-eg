
# For the most part, you should only use
# slots on classes that are going to serve as frequently used data structures in your program
# (e.g., if your program created millions of instances of a particular class)

class Date:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

