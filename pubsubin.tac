from twisted.application import service
from twisted.enterprise import adbapi

from twistar.registry import Registry
from twistar.dbconfig.base import InteractionBase

from pubsubin.control import Router

from config import CONFIG


# Set the config value
Router.setConfig(CONFIG)

InteractionBase.LOG = Router.getConfig('dbdebug')

# Connect to DB
Registry.DBPOOL = adbapi.ConnectionPool(Router.getConfig('dbdriver'),
                                        user=Router.getConfig('dbuser'),
                                        passwd=Router.getConfig('dbpass'),
                                        db=Router.getConfig('dbname'),
                                        host=Router.getConfig('dbhost'))

# Start application
application = service.Application('pubsubin')

# create the router
router = Router(application)
