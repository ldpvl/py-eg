from unittest import TestCase, main
from decimal import Decimal
from itertools import chain
from random import choice, randint
from compression_algorithms.relative_encoding import max_exponent, encode_to_string, decode_from_string


class TestRelativeEncoding(TestCase):
    def setUp(self):
        def generate_random_decimal(i, d):
            return float('%d.%d' % (randint(0, i), randint(0, d)))

        def generate_close_decimals(quantity, base_value, fluctuation_range, exponent=0):
            for _ in range(quantity):
                yield round(Decimal(base_value + choice(fluctuation_range) * (10 ** exponent)), 2)

        def generate_decimals():
            fluctuation_range = list(chain(range(-10, 10, 1),
                                           range(-50, -40, 1),
                                           range(40, 50, 1),
                                           range(100, 105, 1),
                                           range(-105, -100, 1)))
            self.seed_number = generate_random_decimal(999, 999)
            yield from generate_close_decimals(choice(range(50, 100)),
                                               self.seed_number,
                                               fluctuation_range,
                                               -2)

        self.decimals = [str(_) for _ in generate_decimals()]
        exponent = max_exponent(self.decimals)
        self.decimals_encoded = list(encode_to_string(self.decimals, tolerance_factor=0.5, transform_factor=exponent))
        self.decimals_decoded = [str(_) for _ in decode_from_string(self.decimals_encoded, transform_factor=2)]

        write_output_file('output/decimals_original.txt', self.decimals)
        write_output_file('output/decimals_encoded.txt', self.decimals_encoded)
        write_output_file('output/decimals_decoded.txt', self.decimals_decoded)

    def test_encoding_decoding(self):
        for _ in range(20):
            print('Running test cycle:', _,
                  '- length of list of values to encode:', len(self.decimals),
                  '- seed number:', self.seed_number)
            self.assertEqual(self.decimals_decoded, self.decimals)
            self.setUp()

    def test_encoding_prices(self):
        f = open('output/prices_encoded.txt', 'w')
        f.write(','.join(
            encode_to_string((_ for _ in open('resources/prices.txt', 'r')), transform_factor=2, tolerance_factor=1)))


def write_output_file(output_file, values):
    with open(output_file, mode='w') as file:
        file.write('\n'.join(_ for _ in values))


if __name__ == '__main__':
    main()
