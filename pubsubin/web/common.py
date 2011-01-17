from twistler.controllers import NotFound, BaseController
from pubsubin.models import User
from twisted.python import log


def requireLogin(func):
    def wrapper(klass, ctx):
        if getattr(klass.session, 'user_id', None) is not None:
            return func(klass, ctx)
        klass.session.desiredpath = klass.path(clear_query=False)
        klass.message = "You must log in."
        return klass.redirect(klass.path(controller='human', action='login'))
    return wrapper


def _checkOwner(obj, func, klass, ctx, loadRelations):
    if obj is None or obj.user_id != klass.session.user_id:
        return None
    if loadRelations:
        return obj.loadRelations().addCallback(lambda relations: func(klass, ctx, obj, relations))    
    return func(klass, ctx, obj)


def checkOwner(ofklass, loadRelations=False):
    def checkOwnerByType(func):
        def wrapper(klass, ctx):
            if klass.id is None or not klass.id.isdigit():
                return NotFound
            return ofklass.find(klass.id).addCallback(_checkOwner, func, klass, ctx, loadRelations)
        return wrapper
    return checkOwnerByType


def _checkExists(obj, func, klass, ctx, loadRelations):
    if obj is None:
        return None
    if loadRelations:
        return obj.loadRelations().addCallback(lambda relations: func(klass, ctx, obj, relations))
    return func(klass, ctx, obj)


def checkExists(ofklass, param='id', loadRelations=False):
    def checkExistsByType(func):
        def wrapper(klass, ctx):
            klass.addParams(param)
            id = klass.params[param]
            if id is None or not id.isdigit():
                log.msg("ID %s not found" % str(id))
                return NotFound
            return ofklass.find(id).addCallback(_checkExists, func, klass, ctx, loadRelations)
        return wrapper
    return checkExistsByType


class BaseController(BaseController):
    """
    Make our own base controller to handle common stuff like the
    menu and default args.
    """
    def makeMenu(self):
        mname = "Main Nav"
        menu = {mname: []}
        if getattr(self.session, 'user_id', None) is None:
            menu[mname].append(("Log In", self.path('login', controller='human')))
        else:
            menu[mname].append(("Nodes", self.path('index', controller='node')))
            menu[mname].append(("Log Out", self.path('logout', controller='human')))
        menu[mname].append(('About', self.path('about', controller='human')))
        return menu


    def getDefaultViewArgs(self):
        args = { 'menu': self.makeMenu() }
        return args


    def userOwns(self, something):
        if getattr(self.session, 'user_id', None) is None:
            return False
        return something.user_id == self.session.user_id
    

    @property
    def user(self):
        return User.find(self.session.user_id)


    @property
    def router(self):
        return self.appcontroller.router
