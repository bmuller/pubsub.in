from twistler.controllers import StaticController
from pubsubin.control import Router
import os

class FilesController(StaticController):
    PATH = os.path.join(Router.getConfig('templateDir'), "static")

        
