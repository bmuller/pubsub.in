from twisted.application import internet
from twisted.application import service

from nevow import appserver

from twisted.enterprise import adbapi
from twistar.registry import Registry

from pubsubin.web import routes
from pubsubin.control import Router

from config import CONFIG

# Set the config value
Router.setConfig(CONFIG)

# Connect to DB
Registry.DBPOOL = adbapi.ConnectionPool(Router.getConfig('dbdriver'),
                                        user=Router.getConfig('dbuser'),
                                        passwd=Router.getConfig('dbpass'),
                                        db=Router.getConfig('dbname'),
                                        host=Router.getConfig('dbhost'))

# Start application
application = service.Application('pubsubin')
site = appserver.NevowSite(routes.WebRoot())
webServer = internet.TCPServer(Router.getConfig('webport'), site)
webServer.setServiceParent(application)

