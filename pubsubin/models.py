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


class Address(DBObject):
    BELONGSTO = ['user']


class Subscriber(DBObject):
    BELONGSTO = ['user', 'node']


class Publisher(DBObject):
    BELONGSTO = ['user', 'node']


class Message(DBObject):
    BELONGSTO = ['node']

Registry.register(User, Node, Address, Subscriber, Publisher, Message)
