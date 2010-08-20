from twistler.controllers import AppController

from pubsubin.control import Router

from human import HumanController
from files import FilesController

class WebRoot(AppController):
    def __init__(self):
        viewsDir = Router.getConfig('templateDir')
        templateCacheDir = Router.getConfig('templateCacheDir')
        AppController.__init__(self, viewsDir=viewsDir, templateCacheDir=templateCacheDir)

        # these are extra view dirs that controllers should be able to see 
        viewsDirs = ['common']
        self.addController(HumanController, viewDirs=viewsDirs)
        self.addController(FilesController, paths=['static'])
        
