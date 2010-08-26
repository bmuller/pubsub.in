from pubsubin.models import User, Node
from pubsubin.web.common import BaseController, requireLogin, checkOwner

from twisted.python import log

class NodeController(BaseController):
    def __init__(self, *args):
        self.formparams = ['name', 'shortname', 'description', 'is_public']
        BaseController.__init__(self, *args)

    
    @requireLogin
    def index(self, ctx):
        def show(nodes):
            return self.view({'nodes': nodes})
        def getNodes(user):
            return user.nodes.get(limit=10, orderby="id DESC").addCallback(show)
        return self.user.addCallback(getNodes)


    # since starts w/ _ cannot be called as action, so method
    # needs no decoration
    def _save(self, node, erroraction):
        if not node.errors.isEmpty():
            self.message = str(node.errors)
            return self.view(action=erroraction)
        self.message = "Node '%s' saved." % node.name
        return self.redirect(self.path(action='show', id=node.id))        


    @requireLogin
    def create(self, ctx):
        if self.request.method != "POST":
            return self.view()
        self.addParams(*self.formparams)
        self.params['user_id'] = self.session.user_id
        self.params['id'] = None # to prevent haxoring in a node id
        return Node(**self.params).save().addCallback(self._save, 'create')


    @requireLogin
    @checkOwner(Node)
    def show(self, ctx, node):
        return self.view({'node': node})


    @requireLogin
    @checkOwner(Node)
    def edit(self, ctx, node):
        if self.request.method != "POST":
            for prop in self.formparams:
                self.params[prop] = getattr(node, prop)
            return self.view()
        self.addParams(*self.formparams)
        self.params['user_id'] = self.session.user_id
        self.params['id'] = node.id # to prevent haxoring in a node id
        return Node(**self.params).save().addCallback(self._save, 'edit')            

    
