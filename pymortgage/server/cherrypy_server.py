import cherrypy
import os

# static dir defined here for static content
STATIC_DIR = os.path.abspath("%s/../client" % os.path.dirname(__file__))


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


# this class just returns the fixed-chart html file
class GetChart(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(STATIC_DIR, 'index.html'))

from pymortgage.server.REST_Api import RESTServer
from pymortgage.server.d3_api import D3Server
from pymortgage.server.c3_api import C3Server

cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)

api_conf = {
    '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.CORS.on': True}
}

cherrypy.tree.mount(RESTServer(), '/api/amort', config=api_conf)
cherrypy.tree.mount(D3Server(), '/api/d3/amort', config=api_conf)
cherrypy.tree.mount(C3Server(), '/api/c3/amort', config=api_conf)

static_conf = {
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': STATIC_DIR,
    }
}

cherrypy.tree.mount(GetChart(), '/', config=static_conf)

if __name__ == '__main__':
    # assume we're testing locally
    cherrypy.server.bind_addr = ('0.0.0.0', 4001)
    cherrypy.engine.start()
    cherrypy.engine.block()
