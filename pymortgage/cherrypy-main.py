import cherrypy
import os

from amortization import Amortization_Schedule
from d3_schedule import D3_Schedule

# static dir defined here for static content
STATIC_DIR = os.path.abspath(os.path.dirname(__file__))


class REST_Server:
    exposed = True

    def __init__(self):
        self.am_sched = Amortization_Schedule(.0425, 245000, 360)
        self.monthly_d3_sched = D3_Schedule(self.am_sched.schedule)
        self.yearly_d3_sched = D3_Schedule(self.am_sched.get_yearly_schedule())

    # if you were to request /foo/bar?woo=hoo, vpath[0] would be bar, and params would be {'woo': 'hoo'}.
    def GET(self, *vpath, **params):
        if len(vpath) is 0:
            return "Here is the schedule on file: %s" % self.am_sched.schedule
        
        if vpath[0] == 'd3':
            if len(vpath) > 1:
                if vpath[1] == 'year':
                    return self.yearly_d3_sched.get_d3_schedule(by_year=True)

            return self.monthly_d3_sched.get_d3_schedule()

        for month in self.am_sched.schedule:
            if str(month['month']) == str(vpath[0]):
                month_info = month
                return "Here is the info for month %s: %s" % (vpath[0], month_info)
        
        return "No information for month %s" % vpath[0]


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


# this class just returns the chart html file
class Root(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(STATIC_DIR, 'chart.html'))

if __name__ == "__main__":
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    cherrypy.tree.mount(
        REST_Server(), '/api/amort',
        config={'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.CORS.on': True}
        }
    )

    cherrypy.tree.mount(Root(), '/', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': STATIC_DIR,
        },
        '/lib': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '%s/../lib' % STATIC_DIR,
        }
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
