import os
from twisted.python import log
from twisted.web.util import Redirect
from nevow import loaders, rend, tags, inevow, static, stan, url, inevow
from pubsubin.control import Router
from zope.interface import implements

from formless import annotate, webform

from pubsubin.models import User

def requireLogin(func):
    def wrapper(klass, ctx):
        session = inevow.ISession(ctx)
        if getattr(session, 'user_id', None) is not None:
            return func(klass, ctx)
        session.msg = "You must log in."
        session.path_attempt = inevow.IRequest(ctx).URLPath()
        return Redirect(klass.kidpath(ctx, 'login'))
    return wrapper
        

class HumanBase(rend.Page):
    addSlash = True
    
    def __init__(self):
        HumanBase.docFactory = HumanBase.make_loader("layout")
        rend.Page.__init__(self)

    @classmethod
    def make_loader(klass, name):
        layoutpath = os.path.join(Router.getConfig('templateDir'), "%s.xhtml" % name)
        return loaders.xmlfile(layoutpath)

    def make_menu(self, d):
        items = []
        prefix = stan.xml('&raquo; ')
        for key, values in d.items():
            items.append(tags.h3[key])
            ul = [tags.li[prefix, tags.a(href=url)[name]] for (name, url) in values]
            items.append(tags.ul[ul])
        return items

        
    def kidpath(self, ctx, name):
        return inevow.IRequest(ctx).URLPath().child(name)


    def sibpath(self, ctx, name):
        return inevow.IRequest(ctx).URLPath().parentdir().child(name)


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


class SimplePage(HumanBase):
    def __init__(self, contents):
        self.contents = contents
        HumanBase.__init__(self)


    def data_content(self, ctx, data):
        return self.contents



class HumanRoot(HumanBase):
    def child_static(self, ctx):
        staticpath = os.path.join(Router.getConfig('templateDir'), "static")
        return static.File(staticpath)


    def child_index(self, ctx):
        return SimplePage([tags.h3["Header"], tags.p["This is content"]])


    def child_about(self, ctx):
        return SimplePage([tags.h3["Header"], tags.p["This is content"]])        


    def child_login(self, ctx):
        return HumanLogin()


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
    

class HumanLogin(HumanBase):
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


class NodePage(HumanBase):
    nodelist = HumanBase.make_loader("nodelist")
    
    def data_content(self, ctx, data):
        return NodePage.nodelist.load(ctx)


    def render_nodelist(self, ctx, data):
        pat = inevow.IQ(ctx).patternGenerator('node')
        return [pat(data=tags.a(href="http://google.com")['google']) for _ in range(10)]
        return "hello" #[pat['hello'] for _ in range(10)]
