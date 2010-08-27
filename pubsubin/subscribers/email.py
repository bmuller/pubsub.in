from pubsubin.web import routes
from pubsubin.control import Router, BaseSubscriber

from pubsubin.utils import sendEmail

class EMailSubscriber(BaseSubscriber):
    
    def __init__(self, router, application):
        BaseSubscriber.__init__(self, 'email', router, application)
        self.fields = {'to_address': "Address to send emails to."}
        self.requiredFields = ['to_address']
        self.name = "Email"
        self.description = "Send an email to a given address each time a message is posted."
        

    def send(self, msg, config):
        pass


Router.addSubscriber(EMailSubscriber)






