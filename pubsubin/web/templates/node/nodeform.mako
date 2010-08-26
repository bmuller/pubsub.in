<%namespace module="twistler.htmlhelpers" name="h" />
<p>
<%h:form>
Short Name (machine readable): <%h:text name="shortname" value="${shortname}" /><br />
Name (machine readable): <%h:text name="name" value="${name}" /><br />
Description:<br /><%h:textarea name="description" value="${description}" /><br />
<%h:checkbox name="is_public" checked="${is_public}" />Can public post?<br />
<%h:submit/>
</%h:form>
</p>