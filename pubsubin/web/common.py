from twistler import controllers
from pubsubin.models import User
from twisted.python import log

def requireLogin(func):
    def wrapper(klass, ctx):
        if getattr(klass.session, 'user_id', None) is not None:
            return func(klass, ctx)
        klass.session.desiredpath = klass.path()
        klass.params['message'] = "You must log in."
        return klass.redirect(klass.path(controller='human', action='login'))
    return wrapper
        

class BaseController(controllers.BaseController):
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
        args = { 'message': "",
                 'menu': self.makeMenu() }
        return args


    @property
    def user(self):
        return User.find(self.session.user_id)
