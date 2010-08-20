import os
from twisted.python import log
from twisted.web.util import Redirect
from nevow import loaders, rend, tags, inevow, static, stan, url, inevow
from pubsubin.control import Router
from zope.interface import implements

from formless import annotate, webform

from pubsubin.models import User

from twistler.controllers import BaseController


def requireLogin(func):
    def wrapper(klass, ctx):
        session = inevow.ISession(ctx)
        if getattr(session, 'user_id', None) is not None:
            return func(klass, ctx)
        session.msg = "You must log in."
        session.path_attempt = inevow.IRequest(ctx).URLPath()
        return Redirect(klass.kidpath(ctx, 'login'))
    return wrapper
        

class HumanController(BaseController):
    def index(self, ctx):
        return self.view()


    def login(self, ctx):
        return webform.renderForms()
        def dologin(users):
            return self.view({'title': 'title', 'form': users(ctx, None)})
        #return User.all().addCallback(dologin)
        return webform.renderForms().render(ctx, None).addCallback(dologin)
        #args = {'title': "You Must Log In", 'form': webform.renderForms().render(ctx, None)}
        #return self.view(args)
        #d = User.getByUserPass(args['username'], args['password'])
        #return d.addCallback(self._login, args['ctx'])


    def _login(self, user, ctx):
        session = inevow.ISession(ctx)
        if user is not None:
            session.msg = "Welcome!"
            session.user_id = user.id
            if not getattr(session, 'path_attempt', None) is None:
                return Redirect(session.path_attempt)
            return url.here.click('welcome')
        session.msg = "Incorrect password"
        

    def bind_login(self, ctx):
        args = {'username': annotate.String(required=True), 'password': annotate.PasswordEntry(required=True)}
        return self.make_form(args, 'login', 'Login')


    def getDefaultViewArgs(self):
        args = { 'message': "",
                 'menu': self.makeMenu() }
        return args
    

    def makeMenu(self):
        mname = "Main Nav"
        menu = {mname: []}
        if getattr(self.session, 'user_id', None) is None:
            menu[mname].append(("Log In", self.path('login')))
        #else:
        #    menu[mname].append(("Nodes", self.sibpath(ctx, 'nodes')))
        #    menu[mname].append(("Log Out", self.sibpath(ctx, 'logout')))
        #menu[mname].append(('About', self.sibpath(ctx, 'about')))
        return menu



    ################################################

    
    def make_form(self, args, name, action):
        args['ctx'] = annotate.Context()
        arguments = [annotate.Argument(n, v, v.id) for n, v in args.items()]
        method = annotate.Method(arguments=arguments)
        return annotate.MethodBinding(name, method, action=action)        



    def get_user(self, ctx):
        session = inevow.ISession(ctx)        
        return User.find(session.user_id)
