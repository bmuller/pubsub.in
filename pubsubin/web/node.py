from pubsubin.models import User, Node
from pubsubin.web.common import BaseController, requireLogin

from twisted.python import log

class NodeController(BaseController):
    @requireLogin
    def index(self, ctx):
        def show(nodes):
            return self.view({'nodes': nodes})
        def getNodes(user):
            return user.nodes.get(limit=10, orderby="id DESC").addCallback(show)
        return self.user.addCallback(getNodes)


