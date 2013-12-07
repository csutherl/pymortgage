import cherrypy
import json

from amortization import Amortization_Schedule
from d3_schedule import D3_Schedule


class REST_Server:

    def __init__(self):
        self.am_sched = Amortization_Schedule()
        self.d3_sched = D3_Schedule()
        self.schedule = self.am_sched.create_schedule(.0575, 245000, 240)

    def GET(self, id=None):
        if id == None:
            return "Here is the schedule on file: %s" % self.schedule
        
        if str(id) == 'd3':
            return json.dumps(self.d3_sched.comprehend_schedule_for_d3(self.schedule))

        for month in self.schedule:
            if str(month['month']) == str(id): 
                month_info = month
                return "Here is the info for month %s: %s" % (id, month_info)
        
        return "No information for month %s" % id

    exposed = True


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

if __name__ == "__main__":
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.tree.mount(
        REST_Server(), '/api/amort',
            {'/':
                {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.CORS.on': True}
            }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
