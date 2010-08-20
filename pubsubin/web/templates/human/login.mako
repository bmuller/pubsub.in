<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Log In</h3>
<%h:form action="${controller.path('dologin', controller='human')}">
Username: <%h:text name="username" value="${username}" /><br />
Password: <%h:password name="password" /><br />
<%h:submit/>
</%h:form>

<hr />

<h3>Create Account</h3>
<%h:form action="${controller.path('docreateaccount', controller='human')}">
Username: <%h:text name="cusername" value="${cusername}" /><br />
Password: <%h:password name="cpassword" /><br />
Password Again: <%h:password name="cpasswordtwo" /><br />
<%h:submit name="create account"/>
</%h:form>