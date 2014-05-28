__author__ = 'coty'
import unittest
from pymortgage.server.api_helper import parse_params


class TestAPIHelper(unittest.TestCase):
    """
    Class to test the parse_params method and verify that it behaves as expected.
    """
    def test_parse_params_fixed(self):
        with self.assertRaises(ValueError):
            parse_params({'r': 1, 'P': 'test', 'n': 1})

        with self.assertRaises(KeyError):
            parse_params({'a': 'a'})

        try:
            parse_params({'r': 1, 'P': 1, 'n': 1})
        except Exception as e:
            self.fail("Exception throw with valid params. Exception: " + e)

    def test_parse_params_adjustable(self):
        with self.assertRaises(ValueError):
            parse_params({'r': 1, 'P': 1, 'n': 1, 'af': 1, 'ac': 1, 'lc': 'a'})

        try:
            parse_params({'r': 1, 'P': 1, 'n': 1, 'af': 1, 'ac': 1, 'lc': 1})
        except Exception as e:
            self.fail("Exception throw with valid params. Exception: " + e)

    def test_parse_params_optional(self):
        with self.assertRaises(ValueError):
            parse_params({'r': 1, 'P': 1, 'n': 1, 'af': 1, 'ac': 1, 'lc': 1, 't': 'a'})

    def test_parse_params_rates(self):
        with self.assertRaises(Exception):
            parse_params({'r': 1.1, 'P': 1, 'n': 1, 'af': 1, 'ac': 1, 'lc': 1})

        with self.assertRaises(Exception):
            parse_params({'r': 1, 'P': 1, 'n': 1, 'af': 1, 'ac': 1.1, 'lc': 1})

        with self.assertRaises(Exception):
            parse_params({'r': 1, 'P': 1, 'n': 1, 'af': 1, 'ac': 1, 'lc': 1.1})


if __name__ == '__main__':
    unittest.main()
