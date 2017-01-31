from decimal import Decimal


def max_exponent(values):
    return max(abs(Decimal(_).as_tuple().exponent) for _ in values)


def encode(values, transform_factor=0, tolerance_factor=1):
    previous_value = None
    for value in (Decimal(_) for _ in values):
        yield from determine_encoded_value(previous_value, value, tolerance_factor, transform_factor)
        previous_value = value


def determine_encoded_value(previous_value, value, tolerance_factor, transform_factor):
    if previous_value:
        difference = value - previous_value
        if abs(difference) > tolerance_factor:
            yield (value, True)
        else:
            yield (int(difference * (10 ** transform_factor)), False)
    else:
        yield (value, True)


def encode_to_string(values, flag_char='A', transform_factor=0, tolerance_factor=1):
    for value, flag in encode(values, transform_factor, tolerance_factor):
        if flag:
            yield ''.join((str(value), flag_char))
        else:
            yield str(value)


def decode(values, transform_factor=0):
    previous_value = 0
    for value, flag in values:
        if flag:
            previous_value = Decimal(value)
            yield previous_value
        else:
            previous_value += Decimal(value) / (10 ** transform_factor)
            yield previous_value


def decode_from_string(values, flag_char='A', transform_factor=0):
    def transform_values(values, flag_char):
        for value in values:
            if value[-1] == flag_char:
                yield (value[:-1], True)
            else:
                yield (value, False)

    yield from decode(transform_values(values, flag_char), transform_factor)
