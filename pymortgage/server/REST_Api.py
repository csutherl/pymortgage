__author__ = 'coty'

from api_helper import parse_params
import json


class RESTServer:
    exposed = True

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        am_sched = parse_params(params)
        if am_sched is None:
            return "Not enough parameters provided."

        if len(vpath) is 0:
            return json.dumps(am_sched.monthly_schedule)
        else:  # len(vpath) > 0
            if len(vpath) is 1:
                if vpath[0] == 'year':
                    return json.dumps(am_sched.yearly_schedule)
                if vpath[0] == 'month':
                    return json.dumps(am_sched.monthly_schedule)
                else:
                    # test value
                    try:
                        month = int(vpath[0])
                        for month_info in am_sched.monthly_schedule:
                            if str(month_info['month']) == str(month):
                                return json.dumps(month_info)
                    except ValueError:
                        return "Please provide a valid month integer."
            else:  # len(vpath) > 1
                term = vpath[0]

                # quick check to validate month/year
                if term == "year":
                    schedule = am_sched.yearly_schedule
                elif term == "month":
                    schedule = am_sched.monthly_schedule
                else:
                    return "Please request month or year."

                for term_info in schedule:
                    if str(term_info[term]) == str(vpath[1]):
                        return json.dumps(term_info)
        return "No information for %s" % vpath[0]