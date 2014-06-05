#!/usr/bin/env python
import imp
import os

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

#
#  main():
#

if __name__ == '__main__':
   ip   = os.environ['OPENSHIFT_PYTHON_IP']
   port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
   app = imp.load_source('cherrypy_server', 'pymortgage/server/cherrypy_server.py')

   print('Starting CherryPy on %s:%d ... ' % (ip, port))
   app.cherrypy.server.bind_addr = (ip, port)
   app.cherrypy.engine.start()
   app.cherrypy.engine.block()
