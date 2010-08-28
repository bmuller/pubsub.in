<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Add ${subscriber.shortname} Subscription To &quot;${node.name}&quot;</h3>
<p>
<%h:form action="${controller.path('docreate')}">
%for name, desc in subscriber.fields.items():
${infl.humanize(name)}
%if name in subscriber.requiredFields:
(required)
%endif
: <%h:text name="${name}" value="${params[name]}" /><br />
${desc}<br /><br />
%endfor
<%h:hidden name="node_id" value="${node.id}" />
<%h:hidden name="subscriber_name" value="${subscriber.shortname}" />
<%h:submit/>
</%h:form>
</p>
