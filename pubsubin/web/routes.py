import os
from twisted.python import log
from nevow import loaders, rend, tags, inevow, static, stan

from pubsubin.control import Router
from pubsubin.web import human


class WebRoot(rend.Page):
    def renderHTTP(self, ctx):
        request = inevow.IRequest(ctx)
        request.redirect(request.URLPath().child('human').child('index'))
        return ""


    def child_human(self, ctx):
        return human.HumanRoot()
    

