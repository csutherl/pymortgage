__author__ = 'coty'

from api_helper import parse_params
import json
from pymortgage.server.amortization_schedule import AmortizationSchedule


class RESTServer:
    exposed = True

    def __init__(self):
        self.am_monthly_schedule = None
        self.am_yearly_schedule = None

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        self.pps = parse_params(params)
        if self.pps is None:
            return "Not enough parameters provided."

        if len(vpath) is 0:
            return json.dumps(self.getMonthlySchedule())
        else:  # len(vpath) > 0
            if len(vpath) is 1:
                if vpath[0] == 'year':
                    return json.dumps(self.getYearlySchedule())
                if vpath[0] == 'month':
                    return json.dumps(self.getMonthlySchedule())
                else:
                    # test value
                    try:
                        month = int(vpath[0])
                        for month_info in self.getMonthlySchedule():
                            if str(month_info['month']) == str(month):
                                return json.dumps(month_info)
                    except ValueError:
                        return "Please provide a valid month integer."
            else:  # len(vpath) > 1
                term = vpath[0]

                # quick check to validate month/year
                if term == "year":
                    schedule = self.getYearlySchedule()
                elif term == "month":
                    schedule = self.getMonthlySchedule()
                else:
                    return "Please request month or year."

                for term_info in schedule:
                    if str(term_info[term]) == str(vpath[1]):
                        return json.dumps(term_info)
        return "No information for %s" % vpath[0]

    def getMonthlySchedule(self):
        if not self.am_monthly_schedule:
            self.am_monthly_schedule = AmortizationSchedule(self.pps['rate'], self.pps['prin'], self.pps['term'],
                                                            self.pps['tax'], self.pps['ins'], self.pps['adj_freq'],
                                                            self.pps['adj_cap'], self.pps['life_cap'],
                                                            self.pps['extra_pmt'],
                                                            False)

        return self.am_monthly_schedule.monthly_schedule

    def getYearlySchedule(self):
        if not self.am_yearly_schedule:
            self.am_yearly_schedule = AmortizationSchedule(self.pps['rate'], self.pps['prin'], self.pps['term'],
                                                           self.pps['tax'], self.pps['ins'], self.pps['adj_freq'],
                                                           self.pps['adj_cap'], self.pps['life_cap'],
                                                           self.pps['extra_pmt'],
                                                           True)

        return self.am_yearly_schedule.yearly_schedule
