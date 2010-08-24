from pubsubin.models import User, Node
from pubsubin.web.common import BaseController, requireLogin, checkOwner

from twisted.python import log

class NodeController(BaseController):
    @requireLogin
    def index(self, ctx):
        def show(nodes):
            return self.view({'nodes': nodes})
        def getNodes(user):
            return user.nodes.get(limit=10, orderby="id DESC").addCallback(show)
        return self.user.addCallback(getNodes)


    @requireLogin
    def docreate(self, ctx):
        def _save(obj):
            if not obj.errors.isEmpty():
                self.message = str(obj.errors)
                return self.view(action='create')
            self.message = "Node '%s' created." % obj.name
            return self.redirect(self.path(action='index'))
        self.addParams('name', 'shortname', 'description')
        self.params['user_id'] = self.session.user_id
        return Node(**self.params).save().addCallback(_save)


    @requireLogin
    @checkOwner(Node)
    def show(self, ctx, node):
        return "node: %s" % node.shortname
