__author__ = 'coty'

from Api_helper import parse_params
from pymortgage.server.D3_schedule import D3_Schedule


class D3_Server:
    exposed = True

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        am_sched = parse_params(params)

        if am_sched is None:
            return "Not enough parameters provided."

        d3_sched = D3_Schedule(am_sched)
        # rate, P, n, annual_tax, annual_ins, adj_frequency, adj_cap, lifetime_cap
        if len(vpath) > 0:
            if vpath[0] == 'year':
                return d3_sched.yearly_d3_schedule

        return d3_sched.monthly_d3_schedule
