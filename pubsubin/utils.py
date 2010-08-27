from twisted.internet import defer
from twisted.mail import smtp, relaymanager
from twisted.internet import reactor
from twisted.python import log

from cStringIO import StringIO

MXCALCULATOR = relaymanager.MXCalculator()
def getMailExchange(host):
    def cbMX(mxRecord):
        return str(mxRecord.name)
    return MXCALCULATOR.getMX(host).addCallback(cbMX)        

def sendEmail(mailFrom, mailTo, msg, subject=""):
    def dosend(host):
        log.msg("emailing %s (using host %s) from %s" % (mailTo, host, mailFrom))
        d = defer.Deferred()
        msgfile = StringIO("From: %s\nTo: %s\nSubject: %s\n\n%s\n" % (mailFrom, mailTo, subject, msg))
        factory = smtp.ESMTPSenderFactory(None, None, mailFrom, mailTo, msgfile, d, requireAuthentication=False, requireTransportSecurity=False)
        reactor.connectTCP(host, 25, factory)
        return d
    return getMailExchange(mailTo.split("@")[1]).addCallback(dosend)

