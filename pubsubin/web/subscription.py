from pubsubin.models import User, Node, Message, Subscription
from pubsubin.web.common import BaseController, requireLogin, checkOwner, checkExists
from BermiInflector.Inflector import Inflector
from twisted.python import log


class SubscriptionController(BaseController):
    
    @requireLogin
    @checkExists(Node, 'node_id')
    def add(self, ctx, node):
        subtypes = self.appcontroller.router.subscribers.values()
        return self.view({'subtypes': subtypes, 'node': node})


    def _preconfig(self):
        subtypes = self.appcontroller.router.subscribers
        self.addParams('type')
        if self.params['type'] == "" or not subtypes.has_key(self.params['type']):
            self.message = "No such subscriber."
            return False
        subtype = subtypes[self.params['type']]
        self.addParams(*subtype.fields.keys())        
        return subtype


    def _save(self, subscription, erroraction, viewargs):
        if not subscription.errors.isEmpty():
            self.message = str(subscription.errors)
            return self.view(viewargs, action=erroraction)
        self.message = "Subscription added."
        return self.redirect(self.path(action='show', id=subscription.node_id, controller="node"))


    @requireLogin
    @checkExists(Node, 'node_id')
    def create(self, ctx, node):
        subtype = self._preconfig()
        if not subtype:
            return self.redirect(self.path(action='add', node_id=node.id))

        viewargs = {'subtype': subtype, 'node': node, 'infl': Inflector(), 'params': self.params}
        if self.request.method != "POST":
            return self.view(viewargs)

        s = Subscription(user_id=self.session.user_id, node_id=node.id, type_name=subtype.shortname)
        s.setConfig(self.params, subtype)
        return s.save().addCallback(self._save, 'create', viewargs)
    
            
    @requireLogin
    @checkOwner(Subscription, loadRelations=True)
    def edit(self, ctx, sub, relations):
        subtype = self.appcontroller.router.subscribers[sub.type_name]
        node = relations['node']
            
        viewargs = {'subtype': subtype, 'node': node, 'infl': Inflector(), 'params': self.params}
        if self.request.method != "POST":
            for key, value in sub.config.items():
                self.params[key] = value
            return self.view(viewargs)

        self.addParams(*sub.config.keys())
        s = Subscription(**self.params)
        attrs = {'user_id': self.session.user_id, 'node_id': sub.node_id, 'id': sub.id, 'type_name': subtype.shortname}
        s.updateAttrs(attrs)
        s.setConfig(self.params, subtype)
        return s.save().addCallback(self._save, 'edit', viewargs)


    def _delete(self, _):
        self.message = "Subscription deleted."
        self.redirect(self.path(action='show', id=sub.node_id, controller="node"))

    @requireLogin
    @checkOwner(Subscription)
    def delete(self, ctx, sub):
        #bmuller here
        sub.delete().addCallback(self._delete)
