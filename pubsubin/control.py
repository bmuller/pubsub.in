from twisted.python import log
from twisted.internet.defer import DeferredList

import os

import pubsubin
from pubsubin.models import Subscription

class Router:
    CONFIG = {
        'dbdriver': 'MySQLdb',
        'dbhost': 'localhost',
        'templateDir': os.path.join(pubsubin.__path__[0], "web", "templates"),
        'webport': 80,
        'templateCacheDir': None,
        'sslkey': '',
        'sslcrt': '',
        'webportssl': 443,
        'enabledPublishers': ['web', 'webssl'],
        'enabledSubscribers': ['email'],
        'domain': 'localhost',
        'smtpport': 25,
        'dbdebug': False
        }

    PUBLISHERS = []
    SUBSCRIBERS = []

    def __init__(self, application):
        from pubsubin.publishers import *
        from pubsubin.subscribers import *
        
        self.publishers = {}
        self.subscribers = {}
        
        for publisher in Router.PUBLISHERS:
            p = publisher(self, application)
            if p.shortname in Router.getConfig('enabledPublishers'):
                p.start()
                self.publishers[p.shortname] = p
                
        for subscriber in Router.SUBSCRIBERS:
            s = subscriber(self, application)
            if s.shortname in Router.getConfig('enabledSubscribers'):
                s.start()
                self.subscribers[s.shortname] = s


    def subtypeIsEnabled(self, subtypeName):
        return self.subscribers.has_key(subtypeName)


    def getSubtype(self, subtypeName):
        return self.subscribers[subtypeName]


    def publish(self, msg):
        def send(subscribers):
            ds = []
            for subscriber in subscribers:
                d = self.subscribers[subscriber.type_name].send(msg, subscriber)
                ds.append(d)
            return DeferredList(ds)
        return Subscription.getByMessage(msg).addCallback(send)
        

    @classmethod
    def setConfig(klass, config):
        Router.CONFIG.update(config)


    @classmethod
    def getConfig(klass, name):
        if not Router.CONFIG.has_key(name):
            raise RuntimeError, "You must specify the %s configuration value" % name
        return Router.CONFIG[name]


    @classmethod
    def addPublisher(rklass, klass):
        Router.PUBLISHERS.append(klass)


    @classmethod
    def addSubscriber(rklass, klass):
        Router.SUBSCRIBERS.append(klass)



class PublisherType:
    def __init__(self, shortname, router, application):
        self.shortname = shortname
        self.router = router
        self.application = application


    def start(self):
        pass


class SubscriptionType:
    def __init__(self, shortname, router, application):
        self.shortname = shortname
        self.router = router
        self.application = application
        self.fields = {}
        self.requiredFields = []
        self.name = shortname
        self.description = "No description."


    def start(self):
        pass


    def toString(self, sub):
        return "A %s subscription" % sub.name
