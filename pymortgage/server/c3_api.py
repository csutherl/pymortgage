__author__ = 'coty'

from api_helper import parse_params
from pymortgage.server.C3_schedule import C3Schedule
import json


class C3Server:
    exposed = True

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        am_sched = parse_params(params)

        if am_sched is None:
            return "Not enough parameters provided."

        # rate, P, n, annual_tax, annual_ins, adj_frequency, adj_cap, lifetime_cap
        if len(vpath) > 0:
            if vpath[0] == 'year':
                c3_sched = C3Schedule(am_sched)
                return json.dumps(c3_sched.yearly_c3_schedule)
        else:
            c3_sched = C3Schedule(am_sched)
            return json.dumps(c3_sched.monthly_c3_schedule)
