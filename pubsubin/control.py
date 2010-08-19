import os

import pubsubin

class Router:
    CONFIG = {
        'dbdriver': 'MySQLdb',
        'dbhost': 'localhost',
        'templateDir': os.path.join(pubsubin.__path__[0], "web", "templates"),
        'webport': 8080,
        'templateCacheDir': None
        }


    @classmethod
    def setConfig(klass, config):
        Router.CONFIG.update(config)


    @classmethod
    def getConfig(klass, name):
        if not Router.CONFIG.has_key(name):
            raise RuntimeError, "You must specify the %s configuration value" % name
        return Router.CONFIG[name]
