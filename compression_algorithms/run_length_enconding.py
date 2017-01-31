from itertools import groupby


def encode_lazy(values):
    return ((value, len(list(group))) for value, group in groupby(values))


def encode(values):
    values = (_ for _ in values)
    try:
        previous_value = next(values)
        count = 1
        for value in values:
            if previous_value == value:
                count += 1
            else:
                yield (previous_value, count)
                count = 1
                previous_value = value
        yield (previous_value, count)
    except StopIteration:
        return
        yield


def encode_to_string(values, repeats_trigger=3):
    for value, count in encode(values):
        if count > 1 and count >= repeats_trigger:
            yield ''.join(('(', str(value), ',', str(count), ')'))
        else:
            yield from decode(((str(value), count),))


def decode(groups):
    for value, count in groups:
        for _ in range(count):
            yield value


def decode_from_string(values):
    for value in values:
        if value[0] == '(' and value[-1] == ')':
            try:
                item, repeats = value[1:-1].split(',')
                yield from decode(((item, int(repeats)),))
            except ValueError:
                yield value
        else:
            yield value
