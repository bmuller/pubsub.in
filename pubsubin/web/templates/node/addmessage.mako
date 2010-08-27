<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Post Message to &quot;${node.name}&quot;</h3>
<%h:form>
Title: <%h:text name="title" value="${title}" /><br />
Body:<br /><%h:textarea name="body" value="${body}" /><br />
<%h:submit/>
</%h:form>
</p>