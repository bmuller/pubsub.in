from twistar.dbobject import DBObject
import hashlib

class User(DBObject):
    HASMANY = ['nodes', 'addresses']

    @classmethod
    def getByUserPass(klass, username, password):
        password = hashlib.sha1(password).hexdigest()
        return User.find(where=['username = ? AND password = ?', username, password], limit=1)


class Node(DBObject):
    BELONGSTO = ['user']


class Address(DBObject):
    BELONGSTO = ['user']


class Subscriber(DBObject):
    BELONGSTO = ['user', 'node']


class Publisher(DBObject):
    BELONGSTO = ['user', 'node']
