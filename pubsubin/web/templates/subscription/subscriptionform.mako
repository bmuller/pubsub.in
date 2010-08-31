<%namespace module="twistler.htmlhelpers" name="h" />
<p>
<%h:form>
%for name, desc in subtype.fields.items():
${infl.humanize(name)}
%if name in subtype.requiredFields:
(required)
%endif
: <%h:text name="${name}" value="${params[name]}" /><br />
${desc}<br /><br />
%endfor
<%h:hidden name="node_id" value="${node.id}" />
<%h:hidden name="type" value="${subtype.shortname}" />
<%h:submit/>
</%h:form>
</p>
