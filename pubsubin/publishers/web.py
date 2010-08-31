from twisted.application import internet

from pubsubin.web import routes
from pubsubin.control import Router, PublisherType

from nevow import appserver

class WebPublisher(PublisherType):
    def __init__(self, router, application):
        PublisherType.__init__(self, 'web', router, application)

    def start(self):
        site = appserver.NevowSite(routes.WebRoot(self.router))
        webServer = internet.TCPServer(Router.getConfig('webport'), site)
        webServer.setServiceParent(self.application)

Router.addPublisher(WebPublisher)
