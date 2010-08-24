from twistar.dbobject import DBObject
from twistar.registry import Registry
import hashlib


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

    def beforeCreate(self):
        self.shortname = self.shortname.strip()
        self.name = self.name.strip()
        self.description = self.description.strip()
        
Node.validatesLengthOf('name', 'shortname', range=xrange(1,255))
msg = "must be unique in our system.  There is already a node with that shortname."
Node.validatesUniquenessOf('shortname', message=msg)
def shortnameCheck(node):
    if not node.shortname.isalnum():
        node.errors.add('shortname', "can only contain numbers and letters, no spaces or symbols.")
Node.addValidator(shortnameCheck)



class Address(DBObject):
    BELONGSTO = ['user']


class Subscriber(DBObject):
    BELONGSTO = ['user', 'node']


class Publisher(DBObject):
    BELONGSTO = ['user', 'node']


class Message(DBObject):
    BELONGSTO = ['node']

Registry.register(User, Node, Address, Subscriber, Publisher, Message)
