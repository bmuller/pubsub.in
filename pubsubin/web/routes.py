import os
from twisted.python import log
from nevow import loaders, rend, tags, inevow, static
from pubsubin.control import Router


class WebRoot(rend.Page):
    def renderHTTP(self, ctx):
        request = inevow.IRequest(ctx)
        request.redirect(request.URLPath().child('human'))
        return ""


    def child_human(self, ctx):
        return HumanRoot()
    

class HumanBase(rend.Page):
    addSlash = True
    
    def __init__(self):
        self.config = Router.CONFIG
        layoutpath = os.path.join(self.config['templateDir'], "layout.xhtml")
        HumanBase.docFactory = loaders.xmlfile(layoutpath)
        rend.Page.__init__(self)


class HumanRoot(HumanBase):
    def render_content(self, ctx, data):
        return "this is content"


    def child_static(self, ctx):
        staticpath = os.path.join(self.config['templateDir'], "static")
        return static.File(staticpath)

