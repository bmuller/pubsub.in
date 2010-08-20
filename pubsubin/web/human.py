from pubsubin.web.common import BaseController, requireLogin
from pubsubin.models import User

from twisted.python import log

class HumanController(BaseController):
    def logout(self, ctx):
        self.session.user_id = None
        self.params['message'] = "You have been logged out."
        return self.view(action='index')
        

    def dologin(self, ctx):
        self.addParams('username', 'password')
        if self.params['username'] == "" or self.params['password'] == "":
            self.params['message'] = "You must specify a username and password"
            return self.view(action='login')            
        d = User.getByUserPass(self.params['username'], self.params['password'])
        return d.addCallback(self._dologin)


    def _dologin(self, user):
        if user is None:
            self.params['message'] = "User not found with given username and password"
            return self.view(action="login")

        self.session.user_id = user.id
        self.params['message'] = "You have signed in, %s" % user.username
        if getattr(self.session, 'desiredpath', None) is not None:
            return self.redirect(self.session.desiredpath)
        return self.redirect(self.path('main'))
        

    def docreateaccount(self, ctx):
        self.addParams('cusername', 'cpassword', 'cpasswordtwo')
        if self.params['cusername'] == "" or self.params['cpassword'] == "":
            self.params['message'] = "You must specify a username and password"
            return self.view(action='login')
        if self.params['cpassword'] != self.params['cpasswordtwo']:
            self.params['message'] = "Both passwords must match."
            return self.view(action='login')
        user = User(username=self.params['cusername'], password=self.params['cpassword'])
        return user.save().addCallback(self._dologin)
    

    @requireLogin
    def main(self, ctx):
        return self.view()
