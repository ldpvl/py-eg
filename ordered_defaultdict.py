from collections import OrderedDict
from collections import defaultdict


class OrderedDefaultDict(OrderedDict, defaultdict):
    pass


class Cat(object):
    def __init__(self, weight=None, name=None, age=None):
        self.weight = weight
        self.name = name
        self.age = age

    def __str__(self):
        return str(self.name) + ' weighs ' + str(self.weight) + 'kg and is ' + str(self.age) + ' year(s) old.'


ordered_cats = OrderedDefaultDict()
ordered_cats.default_factory = Cat

ordered_cats['black cat'].weight = 5
ordered_cats['black cat'].name = 'Coal'
ordered_cats['black cat'].age = 1
ordered_cats['white cat'].weight = 9
ordered_cats['white cat'].name = 'Paper'
ordered_cats['white cat'].age = 7
ordered_cats['brown cat'].weight = 2
ordered_cats['brown cat'].name = 'Turd'
ordered_cats['brown cat'].age = 12

# This will always print with guaranteed order
print([str(x) for _, x in ordered_cats.items()])

random_cats = defaultdict(Cat)
random_cats['black cat'].weight = 5
random_cats['black cat'].name = 'Coal'
random_cats['black cat'].age = 1
random_cats['white cat'].weight = 9
random_cats['white cat'].name = 'Paper'
random_cats['white cat'].age = 7
random_cats['brown cat'].weight = 2
random_cats['brown cat'].name = 'Turd'
random_cats['brown cat'].age = 12

# This will not guarantee order
print([str(x) for _, x in random_cats.items()])
