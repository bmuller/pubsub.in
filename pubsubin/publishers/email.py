from zope.interface import implements

from twisted.application import internet
from twisted.internet import defer
from twisted.mail import smtp
from twisted.python import log

import email

from pubsubin.control import Router, PublisherType


class MessageDelivery:
    implements(smtp.IMessageDelivery)

    def __init__(self, router):
        self.router = router

    #def receivedHeader(self, helo, origin, recipients):
    #    return "Received: %s message handler" % CONFIG['domain']
    
    def validateFrom(self, helo, origin):
        return origin

    
    def validateTo(self, user):
        if not user.dest.domain.lower().endswith(Router.getConfig('domain')):
            log.err("attempt to send message to an unknown user: \"%s\"" % str(user.dest))
            raise smtp.SMTPBadRcpt(user)
        return lambda: Message(self.router)
        

class Message:
    implements(smtp.IMessage)
    
    def __init__(self, router):
        self.router = router
        self.lines = []

    
    def lineReceived(self, line):
        self.lines.append(line)

    
    def eomReceived(self):
        def doSend(fr):                   
            body = msg.get_payload()
            to = msg['to'][:-len(CONFIG['domain'])-1]       
            if fr is not None:
                self.chathandler.handleNewMessage(to, fr, body)
            else:
                log.err("do not know about sms' from %s" % msg['from'])
            return defer.succeed(None)
        
        msg = email.message_from_string("\n".join(self.lines))        
        self.lines = None
        Node
        return emailToUsername(self.dbpool, msg['from'].lower()).addCallback(doSend)

    
    def connectionLost(self):
        self.lines = None


class SMTPFactory(smtp.SMTPFactory):
    def __init__(self, router):
        smtp.SMTPFactory.__init__(self)
        self.delivery = MessageDelivery(router)

    
    def buildProtocol(self, addr):
        p = smtp.SMTPFactory.buildProtocol(self, addr)
        p.delivery = self.delivery
        return p


class EMailPublisher(PublisherType):
    def __init__(self, router, application):
        PublisherType.__init__(self, 'email', router, application)

    def start(self):
        smtpserver = internet.TCPServer(Router.getConfig('smtpport'), SMTPFactory(self.router))
        smtpserver.setServiceParent(self.application)    

Router.addPublisher(EMailPublisher)

