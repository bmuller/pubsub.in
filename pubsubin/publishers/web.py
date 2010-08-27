from twisted.application import internet

from pubsubin.web import routes
from pubsubin.control import Router, BasePublisher

from nevow import appserver

class WebPublisher(BasePublisher):
    def __init__(self, router, application):
        BasePublisher.__init__(self, 'web', router, application)

    def start(self):
        site = appserver.NevowSite(routes.WebRoot(self.router))
        webServer = internet.TCPServer(Router.getConfig('webport'), site)
        webServer.setServiceParent(self.application)

Router.addPublisher(WebPublisher)
