__author__ = 'coty'

from pymortgage.server.amortization_schedule import AmortizationSchedule

from api_helper import parse_params
from pymortgage.server.D3_schedule import D3Schedule
import json


class D3Server:
    exposed = True

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        # parse and get the parameters
        pps = parse_params(params)

        if pps is None:
            return "Not enough parameters provided."

        # rate, P, n, annual_tax, annual_ins, adj_frequency, adj_cap, lifetime_cap
        if len(vpath) > 0:
            if vpath[0] == 'year':
                am_sched = AmortizationSchedule(pps['rate'], pps['prin'], pps['term'], pps['tax'], pps['ins'],
                                                pps['adj_freq'], pps['adj_cap'], pps['life_cap'], pps['extra_pmt'],
                                                True)
                d3_sched = D3Schedule(am_sched)
                return json.dumps(d3_sched.yearly_d3_schedule)
        else:
            am_sched = AmortizationSchedule(pps['rate'], pps['prin'], pps['term'], pps['tax'], pps['ins'],
                                            pps['adj_freq'], pps['adj_cap'], pps['life_cap'], pps['extra_pmt'], False)
            d3_sched = D3Schedule(am_sched)
            return json.dumps(d3_sched.monthly_d3_schedule)
