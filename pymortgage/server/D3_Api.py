__author__ = 'coty'

from Api_helper import parse_params
from pymortgage.server.D3_schedule import D3Schedule
import json


class D3Server:
    exposed = True

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        am_sched = parse_params(params)

        if am_sched is None:
            return "Not enough parameters provided."

        # rate, P, n, annual_tax, annual_ins, adj_frequency, adj_cap, lifetime_cap
        if len(vpath) > 0:
            if vpath[0] == 'year':
                # TODO: Fix this redundant code...
                if len(vpath) >= 3:
                    try:
                        start = int(vpath[0])
                        end = int(vpath[1])
                    except:
                        raise Exception("Range parameters are not integers.")

                    if start > end:
                        raise Exception("Range start is greater than range end.")

                    d3_sched = D3Schedule(am_sched.get_range('year', start, end), range=True)
                else:
                    d3_sched = D3Schedule(am_sched)

                return json.dumps(d3_sched.yearly_d3_schedule)
            elif len(vpath) >= 2:
                try:
                    start = int(vpath[0])
                    end = int(vpath[1])
                except:
                    raise Exception("Range parameters are not integers.")

                if start > end:
                    raise Exception("Range start is greater than range end.")

                d3_sched = D3Schedule(am_sched.get_range('month', start, end), range=True)
                return json.dumps(d3_sched.monthly_d3_schedule)

        d3_sched = D3Schedule(am_sched)
        return json.dumps(d3_sched.monthly_d3_schedule)
