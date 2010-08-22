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


class Node(DBObject):
    BELONGSTO = ['user']

    def isValid(self):
        if not self.shortname.isalnum():
            return "Shortname can only contain numbers and letters, no spaces or symbols."
        if self.name.strip() == "":
            return "You must specify a name."
        return True

    def beforeCreate(self):
        self.shortname = self.shortname.strip()
        self.name = self.name.strip()
        self.description = self.description.strip()        
        

class Address(DBObject):
    BELONGSTO = ['user']


class Subscriber(DBObject):
    BELONGSTO = ['user', 'node']


class Publisher(DBObject):
    BELONGSTO = ['user', 'node']


class Message(DBObject):
    BELONGSTO = ['node']

Registry.register(User, Node, Address, Subscriber, Publisher, Message)
