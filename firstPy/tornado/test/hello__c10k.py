#coding: utf8
#发送请求测试代码
# ab -n 50000 -c 50 'http://127.0.0.1:8989/'
from gevent import monkey
monkey.patch_all()
import tornado.wsgi
import gevent.wsgi
from gevent.pool import Pool

import signal
import sys

server = None

def signal_term_handler(signal, frame):
    server.stop()
    print 'got SIGTERM'
    print "server stop..."
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

pool = Pool(10000)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    try:
        server = gevent.wsgi.WSGIServer(('', 8989), application, spawn=pool)
        server.serve_forever()
    except KeyboardInterrupt:
        print "server stop..."
        server.stop()

# import os
# print os.path.abspath(__file__)
# print os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))