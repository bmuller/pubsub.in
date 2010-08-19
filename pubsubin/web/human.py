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
    def index(self, ctx, id):
        return "human index"


    def make_menu(self, d):
        items = []
        prefix = stan.xml('&raquo; ')
        for key, values in d.items():
            items.append(tags.h3[key])
            ul = [tags.li[prefix, tags.a(href=url)[name]] for (name, url) in values]
            items.append(tags.ul[ul])
        return items

        
    def data_menu(self, ctx, data):
        session = inevow.ISession(ctx)
        mname = "Main Nav"
        menu = {mname: []}
        if getattr(session, 'user_id', None) is None:
            menu[mname].append(("Log In", self.sibpath(ctx, 'login')))
        else:
            menu[mname].append(("Nodes", self.sibpath(ctx, 'nodes')))
            menu[mname].append(("Log Out", self.sibpath(ctx, 'logout')))
        menu[mname].append(('About', self.sibpath(ctx, 'about')))
        return self.make_menu(menu)


    def make_form(self, args, name, action):
        args['ctx'] = annotate.Context()
        arguments = [annotate.Argument(n, v, v.id) for n, v in args.items()]
        method = annotate.Method(arguments=arguments)
        return annotate.MethodBinding(name, method, action=action)        


    def data_message(self, ctx, data):
        session = inevow.ISession(ctx)
        msg = getattr(session, 'msg', None)
        if msg is not None:
            session.msg = None
            return stan.Tag('div', {'class': 'msg'}, msg)
        return ""


    def get_user(self, ctx):
        session = inevow.ISession(ctx)        
        return User.find(session.user_id)


    def child_logout(self, ctx):
        session = inevow.ISession(ctx)
        session.user_id = None
        session.msg = "You have been logged out."
        return Redirect(self.kidpath(ctx, 'index'))
        

    @requireLogin
    def child_welcome(self, ctx):
        return SimplePage([tags.h3["Header"], tags.p["Welcome! This is content"]])


    def renderHTTP(self, ctx):
        request = inevow.IRequest(ctx)
        request.redirect(self.kidpath(ctx, 'welcome'))
        return ""
        
    @requireLogin
    def child_nodes(self, ctx):
        return NodePage()
    

    def data_content(self, ctx, data):
        return [tags.h3["hello"], webform.renderForms()]


    def login(self, **args):
        d = User.getByUserPass(args['username'], args['password'])
        return d.addCallback(self._login, args['ctx'])


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
