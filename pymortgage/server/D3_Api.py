__author__ = 'coty'

from pymortgage.server.amortization import Amortization_Schedule
from pymortgage.server.D3_schedule import D3_Schedule


class D3_Server:
    exposed = True

    def __init__(self):
        self.am_sched = Amortization_Schedule(.0425, 245000, 360, 1836, 1056, 2, .01, .06)
        self.monthly_d3_sched = D3_Schedule(self.am_sched.monthly_schedule)
        self.yearly_d3_sched = D3_Schedule(self.am_sched.yearly_schedule)

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        if len(vpath) > 0:
            if vpath[0] == 'year':
                return self.yearly_d3_sched.get_d3_schedule(by_year=True)

        return self.monthly_d3_sched.get_d3_schedule()
