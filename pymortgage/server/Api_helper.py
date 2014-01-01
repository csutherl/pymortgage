__author__ = 'coty'

from pymortgage.server.amortization import Amortization_Schedule


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
    '''
    adjustable = False

    try:
        if 1 < params['r'] < 0:
            raise Exception("Rate is not expressed as decimal.")
        elif params['P'] is None:
            raise Exception("Principal not provided.")
        elif params['n'] is None:
            raise Exception("Terms not provided.")
        elif params['t'] is None:
            raise Exception("Taxes not provided.")
        elif params['i'] is None:
            raise Exception("Insurance not provided.")
    except Exception as e:
        print "There was an exception: %s" % e.message
        return None

    try:
        if (params['af'] is None and params['ac'] is None and params['lc'] is None) or \
            (params['af'] is not None and params['ac'] is not None and params['lc'] is not None):
            if 1 < params['ac'] < 0:
                raise Exception("Adjustment cap is not expressed as decimal.")
            elif 1 < params['lc'] < 0:
                raise Exception("Lifetime cap is not expressed as decimal.")
            else:
                adjustable = True
        else:
            raise Exception("Partial values provided for Adjustable mortgage.")
    except Exception as e:
        print "There was an exception: %s" % e.message
        return None

    p = params  # shorting the var name :)
    try:
        rate = float(p['r'])
        prin = int(p['P'])
        term = int(p['n'])
        tax = int(p['t'])
        ins = int(p['i'])
    except Exception as e:
        print "There was an exception: %s" % e.message
        return None

    if adjustable:
        try:
            adj_freq = int(p['af'])
            adj_cap = float(p['ac'])
            life_cap = float(p['lc'])
        except Exception as e:
            print "There was an exception: %s" % e.message
            return None
        return Amortization_Schedule(rate, prin, term, tax, ins, adj_freq, adj_cap, life_cap)
    else:
        return Amortization_Schedule(rate, prin, term, tax, ins)
