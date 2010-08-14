import os

import pubsubin

class Router:
    CONFIG = {
        'templateDir': os.path.join(pubsubin.__path__[0], "web", "templates")
        }


    @classmethod
    def setConfig(klass, config):
        Router.CONFIG.update(config)
