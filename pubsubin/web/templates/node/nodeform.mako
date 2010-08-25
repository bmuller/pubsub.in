<%namespace module="twistler.htmlhelpers" name="h" />
<%h:form>
Short Name (machine readable): <%h:text name="shortname" value="${shortname}" /><br />
Name (machine readable): <%h:text name="name" value="${name}" /><br />
Description:<br /><%h:textarea name="description" value="${description}" /><br />
<%h:submit/>
</%h:form>
