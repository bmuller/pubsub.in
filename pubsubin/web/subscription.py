from pubsubin.models import User, Node, Message, Subscriber
from pubsubin.web.common import BaseController, requireLogin, checkOwner, checkExists
from BermiInflector.Inflector import Inflector
from twisted.python import log


class SubscriptionController(BaseController):
    
    @requireLogin
    @checkExists(Node, 'node_id')
    def add(self, ctx, node):
        subscribers = self.appcontroller.router.subscribers.values()
        return self.view({'subscribers': subscribers, 'node': node})

    def _preconfig(self):
        subscribers = self.appcontroller.router.subscribers
        self.addParams('subscriber_name')
        if self.params['subscriber_name'] == "" or not subscribers.has_key(self.params['subscriber_name']):
            self.message = "No such subscriber."
            return False
        subscriber = subscribers[self.params['subscriber_name']]
        self.addParams(*subscriber.fields.keys())        
        return subscriber


    @requireLogin
    @checkExists(Node, 'node_id')
    def create(self, ctx, node):
        subscriber = self._preconfig()
        if not subscriber:
            return self.redirect(self.path(action='add', id=node.id))        
        return self.view({'subscriber': subscriber, 'node': node, 'infl': Inflector(), 'params': self.params})


    @requireLogin
    @checkExists(Node, 'node_id')
    def docreate(self, ctx, node):
        def _save(subscriber):
            self.message = "Subscription added."
            return self.redirect(self.path(controller='node', action='show', id=node.id))
        subscriber = self._preconfig()
        if not subscriber:
            return self.redirect(self.path(action='add', id=node.id))
        config = subscriber.encodeConfig(self.params)
        if config is False:
            self.message = "You must fill out all required fields."
            args = {'subscriber': subscriber, 'node': node, 'infl': Inflector(), 'params': self.params}
            return self.view(args, action='configure')
        s = Subscriber(user_id=self.session.user_id, node_id=node.id, service_name=subscriber.shortname, config=config)
        return s.save().addCallback(_save)
    
            
