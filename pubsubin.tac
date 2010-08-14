from twisted.application import internet
from twisted.application import service

from nevow import appserver

from pubsubin.web import routes
from pubsubin.control import Router

config = { 
    }   

Router.setConfig(config)

application = service.Application('pubsubin')
site = appserver.NevowSite(routes.WebRoot())
webServer = internet.TCPServer(8080, site)
webServer.setServiceParent(application)

