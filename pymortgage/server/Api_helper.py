__author__ = 'coty'

from pymortgage.server.amortization_schedule import Amortization_Schedule
import traceback


def parse_params(params):
    '''
        Params:
        'r' = rate
        'P' = principal
        'n' = term
        't' = taxes
        'i' = insurance
        'af' = adjustment frequency (in years)
        'ac' = adjustment cap (percent in decimal form)
        'lc' = lifetime cap (percent in decimal form)
        'e' = extra payment amount
    '''
    adjustable = False

    # check keys and conversions
    p = params  # shorting the var name :)

    # always required
    try:
        rate = float(p['r'])
        prin = int(p['P'])
        term = int(p['n'])
        tax = int(p['t'])
        ins = int(p['i'])
    except KeyError as ke:
        print "A required parameter is missing: %s" % ke.message
        return None
    except ValueError as ve:
        print "A required parameter has an invalid value: %s" % ve.message
        return None

    # only required for adjustable
    try:
        adj_freq = int(p['af'])
        adj_cap = float(p['ac'])
        life_cap = float(p['lc'])

        adjustable = True
    except KeyError:
        adjustable = False
    except ValueError as ve:
        print "A parameter has an invalid value: %s" % ve.message
        return None

    # always optional values
    try:
        extra_pmt = int(p['e'])
    except KeyError:
        extra_pmt = 0
    except ValueError as ve:
        print "A parameter has an invalid value: %s" % ve.message
        return None

    # check values
    try:
        if 1 < rate < 0:
            raise Exception("Rate is not expressed as decimal.")
        if adjustable:
            if 1 < adj_cap < 0:
                raise Exception("Adjustment cap is not expressed as decimal.")
            elif 1 < life_cap < 0:
                raise Exception("Lifetime cap is not expressed as decimal.")
    except Exception as e:
        print e.message
        return None

    if adjustable:
        return Amortization_Schedule(rate, prin, term, tax, ins, adj_freq, adj_cap, life_cap, extra_pmt)
    else:
        return Amortization_Schedule(rate, prin, term, tax, ins, extra_pmt=extra_pmt)
