from pubsubin.models import User, Node, Message
from pubsubin.web.common import BaseController, requireLogin, checkOwner, checkExists
from BermiInflector.Inflector import Inflector
from twisted.python import log


class SubscriptionController(BaseController):
    
    @requireLogin
    @checkExists(Node)
    def add(self, ctx, node):
        subscribers = self.appcontroller.router.subscribers.values()
        return self.view({'subscribers': subscribers, 'node': node})


    @requireLogin
    @checkExists(Node)
    def configure(self, ctx, node):
        subscribers = self.appcontroller.router.subscribers
        self.addParams('subscriber_name')
        if self.params['subscriber_name'] == "" or not subscribers.has_key(self.params['subscriber_name']):
            self.message = "No such subscriber again."
            return self.redirect(self.path(action='add', id=node.id))
        
        subscriber = subscribers[self.params['subscriber_name']]
        self.addParams(*subscriber.fields.keys())
        return self.view({'subscriber': subscriber, 'node': node, 'infl': Inflector(), 'params': self.params})


    @requireLogin
    @checkExists(Node)
    def doconfigure(self, ctx, node):
        subscribers = self.appcontroller.router.subscribers
        self.addParams('subscriber_name')
        if self.params['subscriber_name'] == "" or not subscribers.has_key(self.params['subscriber_name']):
            self.message = "No such subscriber again."
            return self.redirect(self.path(action='add', id=node.id))

        subscriber = subscribers[self.params['subscriber_name']]
        self.addParams(*subscriber.fields.keys())

        s = Subscriber(user_id=self.session.user_id, node_id=node.id, service_name=subscriber.shortname)
        s.config = subscriber.encodeConfig(self.params)
        
        return self.view({'subscriber': subscriber, 'node': node, 'infl': Inflector(), 'params': self.params})

    
            
