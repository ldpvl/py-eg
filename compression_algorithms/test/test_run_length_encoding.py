from unittest import TestCase, main
from random import randrange
from compression_algorithms.run_length_enconding import *


class TestRunLengthEncoding(TestCase):
    def setUp(self):
        self.values = [v for g in ([_] * randrange(5) for _ in range(randrange(5), randrange(10))) for v in g]

    def test_encode_lazy_decode(self):
        for _ in range(10):
            self.setUp()
            encoded = list(encode_lazy(self.values))
            print('Running test cycle:', _)
            print('List of values:', self.values)
            print('Encoded result:', encoded)
            self.assert_results(encoded)

    def test_encode(self):
        line = '146.61A,1,-1,0,0,0,0,0,0,0,0,1,1,-1,0,0,0,0,0,1'
        expected = ['146.61A', 1, '1', 1, '-1', 1, '0', 8, '1', 2, '-1', 1, '0', 5, '1', 1]
        self.assertEqual(expected, [v for g in encode(line.split(',')) for v in g])
        self.assertEqual(line, ','.join(decode(encode(line.split(',')))))

    def test_encode_decode(self):
        encoded = list(encode(self.values))
        self.assert_results(encoded)

    def test_encode_to_string(self):
        line = '146.61A,1,-1,0,0,0,0,0,0,0,0,1,1,-1,0,0,0,0,0,1'
        expected = ['146.61A', '1', '-1', '(0,8)', '1', '1', '-1', '(0,5)', '1']
        self.assertEqual(expected, list(encode_to_string(line.split(','), repeats_trigger=3)))
        self.assertEqual(line, ','.join(decode_from_string(expected)))
        self.assertEqual([str(_) for _ in self.values], list(decode_from_string(encode_to_string(self.values))))

    def assert_results(self, encoded):
        decoded = list(decode(encoded))
        print('Decoded result:', decoded)
        for encoded_value, expected_value in zip(self.values, decoded):
            self.assertEqual(encoded_value, expected_value)


if __name__ == '__main__':
    main()
