import tornado.ioloop
import tornado.web
import tornado.websocket

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class MainHandler2(tornado.web.RequestHandler):
    def get(self):
        self.write("This is a test")

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test", MainHandler2),
    (r"/websocket", EchoWebSocket),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()