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


    @requireLogin
    def docreate(self, ctx):
        self.addParams('name', 'shortname', 'description')
        self.params['user_id'] = self.session.user_id
        node = Node(**self.params)
        result = node.isValid()
        if not result == True:
            self.params['message'] = result
            return self.view(action="create")
        return "hello"
        #return self.redirect(self.path("show"))
