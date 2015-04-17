import tornado.ioloop
import tornado.web
import os
import json

from WSNData import nodeInfo
from WSNData.receptionRatio import receptionDict, receptionMeta

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./pages/index.html", arg="WSN")

class RootHtmlHandler(tornado.web.RequestHandler):
    def get(self, html):
        print 'RootHtmlHandler: html:', html
        if not os.path.exists(html):
            self.send_error(404)
        else:
            self.render(html, title=html)

class NodeInfoHandler(tornado.web.RequestHandler):
    def get(self):
        output = json.dumps(nodeInfo.NodeInfo)
        self.write(output)

class ReceptionRatioHandler(tornado.web.RequestHandler):
    def get(self, args):
        # date= &hour= &min=
        date = int(self.get_argument("date"))
        hour = int(self.get_argument("hour"))
        minute = int(self.get_argument("min"))
        print "Reception:", date, hour, minute
        self.write(json.dumps(receptionDict[date][hour][minute]))

class ReceptionMetaHandler(tornado.web.RequestHandler):
    def get(self):
        print "ReceptionMetaHandler"
        self.write(json.dumps(receptionMeta))

settings = \
    {
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(.*.html)", RootHtmlHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/Data/NodeInfo", NodeInfoHandler),
    (r"/Rep/meta", ReceptionMetaHandler),
    (r"/Rep/(.*)", ReceptionRatioHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()