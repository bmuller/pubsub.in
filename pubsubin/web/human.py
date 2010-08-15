import os
from twisted.python import log
from twisted.web.util import Redirect
from nevow import loaders, rend, tags, inevow, static, stan, url
from pubsubin.control import Router
from zope.interface import implements

from formless import annotate, webform


def requireLogin(func):
    def wrapper(klass, ctx):
        session = inevow.ISession(ctx)
        if getattr(session, 'loggedin', 0):
            return func(klass, ctx)
        session.msg = "You must log in."
        return Redirect(klass.kidpath(ctx, 'login'))
    return wrapper
        

class HumanBase(rend.Page):
    addSlash = True
    
    def __init__(self):
        self.config = Router.CONFIG
        layoutpath = os.path.join(self.config['templateDir'], "layout.xhtml")
        HumanBase.docFactory = loaders.xmlfile(layoutpath)
        rend.Page.__init__(self)


    def make_menu(self, d):
        items = []
        prefix = stan.xml('&raquo; ')
        for key, value in d.items():
            items.append(tags.h3[key])
            ul = [tags.li[prefix, tags.a(href=url)[name]] for name, url in value.items()]
            items.append(tags.ul[ul])
        return items

        
    def kidpath(self, ctx, name):
        return inevow.IRequest(ctx).URLPath().child(name)


    def sibpath(self, ctx, name):
        return inevow.IRequest(ctx).URLPath().parentdir().child(name)


    def data_menu(self, ctx, data):
        session = inevow.ISession(ctx)
        mname = "Main Nav"
        menu = {mname: {'About': self.sibpath(ctx, 'about')}}
        if not getattr(session, 'loggedin', 0):
            menu[mname]["Log In"] = self.sibpath(ctx, 'login')
        else:
            menu[mname]["Log Out"] = self.sibpath(ctx, 'logout')            
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


class SimplePage(HumanBase):
    def __init__(self, contents):
        self.contents = contents
        HumanBase.__init__(self)


    def data_content(self, ctx, data):
        return self.contents



class HumanRoot(HumanBase):
    def child_static(self, ctx):
        staticpath = os.path.join(self.config['templateDir'], "static")
        return static.File(staticpath)


    def child_index(self, ctx):
        return SimplePage([tags.h3["Header"], tags.p["This is content"]])


    def child_about(self, ctx):
        return SimplePage([tags.h3["Header"], tags.p["This is content"]])        


    def child_login(self, ctx):
        return HumanLogin()


    def child_logout(self, ctx):
        session = inevow.ISession(ctx)
        session.loggedin = False
        session.msg = "You have been logged out."
        return Redirect(self.kidpath(ctx, 'index'))
        

    @requireLogin
    def child_welcome(self, ctx):
        return SimplePage([tags.h3["Header"], tags.p["Welcome! This is content"]])


    def renderHTTP(self, ctx):
        request = inevow.IRequest(ctx)
        request.redirect(self.kidpath(ctx, 'welcome'))
        return ""
        


class HumanLogin(HumanBase):
    def data_content(self, ctx, data):
        return [tags.h3["hello"], webform.renderForms()]


    def login(self, **args):
        session = inevow.ISession(args['ctx'])            
        if args['username'] == "user" and args['password'] == "pass":
            session.loggedin = True
            session.msg = "Welcome!"
            return url.here.click('welcome')
        session.msg = "Incorrect password"
        

    def bind_login(self, ctx):
        args = {'username': annotate.String(required=True), 'password': annotate.PasswordEntry(required=True)}
        return self.make_form(args, 'login', 'Login')
