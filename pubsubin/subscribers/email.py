from pubsubin.web import routes
from pubsubin.control import Router, SubscriptionType

from pubsubin.utils import sendEmail


class EMailSubscriptionType(SubscriptionType):
    def __init__(self, router, application):
        SubscriptionType.__init__(self, 'email', router, application)
        self.fields = {'to_address': "Address to send emails to."}
        self.requiredFields = ['to_address']
        self.name = "Email"
        self.description = "Send an email to a given address each time a message is posted."
        

    def send(self, msg, subscriber):
        def doSend(node):
            toaddy = subscriber.config['to_address']
            fromaddy = "%s-%s@%s" % (node.shortname, node.access_key, self.router.getConfig('domain'))
            sendEmail(fromaddy, toaddy, msg.body, msg.title)
        return subscriber.node.get().addCallback(doSend)        


    def toString(self, emailsub):
        return "send emails to %s" % emailsub.config['to_address']        

Router.addSubscriber(EMailSubscriptionType)






