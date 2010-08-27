from twisted.application import internet

# the following try/except/if has been taken per recommendation from
# http://twistedmatrix.com/trac/browser/tags/releases/twisted-10.0.0//twisted/internet/ssl.py
try:
    from twisted.internet import ssl
except ImportError:
    ssl = None
if ssl and not ssl.supported:
    ssl = None                    

from pubsubin.web import routes
from pubsubin.control import Router, BasePublisher

from nevow import appserver


class WebSSLPublisher(BasePublisher):
    def __init__(self, router, application):
        BasePublisher.__init__(self, 'webssl', router, application)

    def start(self):
        site = appserver.NevowSite(routes.WebRoot(self.router))
        sslContext = ssl.DefaultOpenSSLContextFactory(Router.getConfig('sslkey'), Router.getConfig('sslcrt'))
        webServerSSL = internet.SSLServer(Router.getConfig('webportssl'), site, sslContext)
        webServerSSL.setServiceParent(self.application)

Router.addPublisher(WebSSLPublisher)
