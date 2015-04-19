import tornado.ioloop
import tornado.web
import os
import json

from WSNData import nodeInfo
from WSNData.receptionRatio import receptionDict, receptionMeta
import time

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

from dateutil import rrule
from datetime import datetime, timedelta

class ReceptionDurationHandler(tornado.web.RequestHandler):
    def get(self, args):
        s = self.get_argument("s")
        e = self.get_argument("e")
        st = datetime.strptime(s, '%Y-%m-%d %H-%M-%S')
        et = datetime.strptime(e, '%Y-%m-%d %H-%M-%S')
        print "ReceptionDurationHandler", st, et
        responseArray = []
        for dt in rrule.rrule(rrule.MINUTELY, dtstart=st, until=et):
            responseArray += receptionDict[dt.day][dt.hour][dt.minute]
        self.write(json.dumps(responseArray))

settings = \
    {
        "static_path": os.path.join(os.path.dirname(__file__), "pages/static")
    }
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(.*.html)", RootHtmlHandler),
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/Data/NodeInfo", NodeInfoHandler),
    (r"/Rep/meta", ReceptionMetaHandler),
    (r"/Rep/duration/(.*)", ReceptionDurationHandler),
    (r"/Rep/(.*)", ReceptionRatioHandler),
])

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()