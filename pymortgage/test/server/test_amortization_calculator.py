__author__ = 'coty'
import unittest
from pymortgage.server.amortization_calculator import calc_amortization


class TestCalcAmortization(unittest.TestCase):
    """
    Class to test the calc_amortization method and verify that it return correct values.
    """
    def test_calc_amorization(self):
        # initial test to check first month
        # TODO: Put actual values here from a different algorithm to check
        test = calc_amortization(.045, 240000, 360)
        expected = {"amount": 1216.04, "interest": 900, "principal": 316.04, "monthly_rate": 0.00375}

        self.assertEqual(test, expected)

if __name__ == '__main__':
    unittest.main()