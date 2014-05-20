__author__ = 'coty'

from math import pow


def calc_amortization(rate, P, n):
    """
    Method to calculate amortization given rate, principal, and terms remaining.
    """
    # calc monthly interest rate
    # doing this funky conversion stuff to drop off the remaining digits instead of round up.
    i = float(str(rate / 12)[:10])

    # calc amortization for a single month
    amort = round(((i * P * pow((1 + i), n)) / (pow((1 + i), n) - 1)), 2)

    # calc monthly interest
    mi = round((P * i), 2)

    # calc monthly principal portion
    mp = round((amort - mi), 2)

    # return array of amount/interest/principal/monthly_rate
    return {"amount": amort, "interest": mi, "principal": mp, "monthly_rate": i}
