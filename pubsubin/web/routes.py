from twistler.controllers import AppController

from pubsubin.control import Router

from human import HumanController
from files import FilesController

class WebRoot(AppController):
    def __init__(self):
        viewsDir = Router.getConfig('templateDir')
        templateCacheDir = Router.getConfig('templateCacheDir')
        AppController.__init__(self, viewsDir=viewsDir, templateCacheDir=templateCacheDir)
        
        self.addController(HumanController)
        self.addController(FilesController, ['static'])
        
