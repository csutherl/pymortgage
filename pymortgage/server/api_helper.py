__author__ = 'coty'

from pymortgage.server.amortization_schedule import AmortizationSchedule


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
    # check keys and conversions
    p = params  # shorting the var name :)

    # always required
    try:
        rate = float(p['r'])
        prin = int(p['P'])
        term = int(p['n'])
    except KeyError as ke:
        raise KeyError("A required parameter is missing: %s" % ke.message)
    except ValueError as ve:
        raise ValueError("A required parameter has an invalid value: %s" % ve.message)

    # only required for adjustable
    try:
        adj_freq = int(p['af'])
        adj_cap = float(p['ac'])
        life_cap = float(p['lc'])

        adjustable = True
    except KeyError:
        adjustable = False
    except ValueError as ve:
        raise ValueError("A parameter has an invalid value: %s" % ve.message)

    # always optional values
    try:
        try:
            tax = int(p['t'])
        except KeyError:
            tax = 0
        try:
            ins = int(p['i'])
        except KeyError:
            ins = 0
        try:
            extra_pmt = int(p['e'])
        except KeyError:
            extra_pmt = 0
    except ValueError as ve:
        raise ValueError("A parameter has an invalid value: %s" % ve.message)

    # check values
    if rate < 0 or rate > 1:
        raise Exception("Rate is not expressed as decimal.")
    if adjustable:
        if adj_cap < 0 or adj_cap > 1:
            raise Exception("Adjustment cap is not expressed as decimal.")
        elif life_cap < 0 or life_cap > 1:
            raise Exception("Lifetime cap is not expressed as decimal.")

    if adjustable:
        return AmortizationSchedule(rate, prin, term, tax, ins, adj_freq, adj_cap, life_cap, extra_pmt)
    else:
        return AmortizationSchedule(rate, prin, term, tax, ins, extra_pmt=extra_pmt)
