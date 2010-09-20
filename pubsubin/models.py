from twistar.dbobject import DBObject
from twistar.registry import Registry
from twisted.python import log

import hashlib, uuid, cPickle


class User(DBObject):
    HASMANY = ['nodes', 'addresses']

    @classmethod
    def getByUserPass(klass, username, password):
        password = hashlib.sha1(password).hexdigest()
        return User.find(where=['username = ? AND password = ?', username, password], limit=1)


    def beforeCreate(self):
        self.password = hashlib.sha1(self.password).hexdigest()
        
User.validatesLengthOf('username', 'password', range=xrange(1,255))



class Node(DBObject):
    BELONGSTO = ['user']
    HASMANY = ['messages', 'subscriptions']

    def beforeSave(self):
        self.shortname = self.shortname.strip()
        self.name = self.name.strip()
        self.description = self.description.strip()

    def beforeCreate(self):
        self.access_key = uuid.uuid4().hex
        self.access_password = uuid.uuid4().hex
        
Node.validatesLengthOf('name', 'shortname', range=xrange(1,255))
msg = "must be unique in our system.  There is already a node with that shortname."
Node.validatesUniquenessOf('shortname', message=msg)
Node.validatesUniquenessOf('access_key', message="Please try saving again.")
def shortnameCheck(node):
    if not node.shortname.isalnum():
        node.errors.add('shortname', "can only contain numbers and letters, no spaces or symbols.")
Node.addValidator(shortnameCheck)



class Address(DBObject):
    BELONGSTO = ['user']


class Subscription(DBObject):
    BELONGSTO = ['user', 'node']

    def getByMessage(self, msg):
        """
        Get every subscriber that should get this message.
        """
        return Subscription.find(where=['node_id = ?', msg.node_id])


    def afterInit(self):
        """
        depickle our config
        """
        if hasattr(self, 'config'):
            self.config = cPickle.loads(self.config)


    def beforeSave(self):
        log.msg("About to save sub.  config before is: '%s'" % str(self.config))        
        self.config = cPickle.dumps(self.config)
        log.msg("About to save sub.  config after is: '%s'" % str(self.config))


    def setConfig(self, config, subtype):
        self.config = {}
        for field in subtype.fields.keys():
            if field in subtype.requiredFields and config.get(field, "") == "":
                self.errors.add(field, "cannot be blank")
            self.config[field] = config.get(field, "")
                
        

class Publisher(DBObject):
    BELONGSTO = ['user', 'node']


class Message(DBObject):
    BELONGSTO = ['node']

Message.validatesPresenceOf('body')

Registry.register(User, Node, Address, Subscription, Publisher, Message)
