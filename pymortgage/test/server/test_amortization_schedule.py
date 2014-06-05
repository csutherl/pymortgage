__author__ = 'coty'
import unittest
from pymortgage.server.amortization_schedule import AmortizationSchedule


class TestAmortizationSchedule(unittest.TestCase):
    """
    Class to test the AmortizationSchedule class and verify that it behaves as expected.
    """
    def setUp(self):
        # fixed 5% on 240k at 30 years
        self.FixedSchedule = AmortizationSchedule(.05, 240000, 360)
        # adjustable 5% on 240k at 30 years. 5 yr adjustment, 2% adjustment cap, 6% lifetime cap
        self.ARMSchedule = AmortizationSchedule(.05, 240000, 360, 0, 0, 5, .02, .06)

    def test_fixed_schedule_monthly(self):
        # TODO: Put actual values here from a different algorithm to check
        actual = self.FixedSchedule.monthly_schedule[0]  # check first month
        expected = {"amount": 1216.04, "interest": 900, "principal": 316.04, "monthly_rate": 0.00375}
        self.assertEqual(actual, expected)

    def test_fixed_schedule_yearly(self):
        # TODO: Put actual values here from a different algorithm to check
        actual = self.FixedSchedule.yearly_schedule[0]  # check first year
        expected = {"amount": 1216.04, "interest": 900, "principal": 316.04, "monthly_rate": 0.00375}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
