__author__ = 'coty'
import unittest
from pymortgage.server.d3_api import D3Server


class TestD3API(unittest.TestCase):
    def setUp(self):
        self.server = D3Server()
        self.vpath = ['year']
        self.params = {'r': 1, 'P': 1, 'n': 1}  # need to reference these with ** to get the keyword args

    def test_GET(self):
        import json
        actual = len(json.loads(self.server.GET(*self.vpath, **self.params)))
        # check length against number of keys
        expected = 7

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
