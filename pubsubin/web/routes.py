from twistler.controllers import AppController

from human import HumanController
from files import FilesController

class WebRoot(AppController):
    def __init__(self):
        WebRoot.addController(HumanController)
        WebRoot.addController(FilesController, ['static'])
