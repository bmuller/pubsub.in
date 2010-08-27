from pubsubin.models import User, Node, Message
from pubsubin.web.common import BaseController, requireLogin, checkOwner, checkExists

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
        def _show(msgs):
            return self.view({'node': node, 'msgs': msgs})
        return node.messages.get().addCallback(_show)
        


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


    def _saveMsg(self, msg, node):
        def showResult():
            self.message = "Message entitled '%s' published." % msg.title
            return self.redirect(self.path(action='show', id=node.id))
        
        if not msg.errors.isEmpty():
            self.message = str(msg.errors)
            return self.view({'node': node}, action='addmessage')
        return self.appcontroller.router.publish(msg).addCallback(showResult)


    @requireLogin
    @checkOwner(Node)
    def addmessage(self, ctx, node):
        self.addParams('title', 'body')
        if self.request.method != "POST":
            return self.view({'node': node})
        self.params['id'] = None
        self.params['node_id'] = self.id
        return Message(**self.params).save().addCallback(self._saveMsg, node)


    @checkExists(Message)
    def viewmsg(self, ctx, message):
        def checkPerms(node):
            if not self.userOwns(node) and not node.is_public:
                self.message = "You don't have permission to view that node.  You may just need to log in first."
                return self.redirect(self.path(controller='human', action='index', id=None))
            return self.view({'msg': message})
        return message.node.get().addCallback(checkPerms)
