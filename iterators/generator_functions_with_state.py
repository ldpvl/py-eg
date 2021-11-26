from collections import deque


class iterable_with_history:
    def __init__(self, items, history_len=5):
        self.items = items
        self.history = deque(maxlen=history_len)

    def __iter__(self):
        for index, item in enumerate(self.items):
            self.history.append((index, item))
            yield item


x = [5, 6, 7, 1, 2, 3]
y = iterable_with_history(x)

for _ in y:
    print(_)
    print(y.history)
