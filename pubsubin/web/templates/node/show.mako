<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Node: ${node.name}</h3>
<p>Shortname: ${node.shortname | h}</p>
<p>Description: ${node.description | h}</p>
<p>Access Key: ${node.access_key}</p>
<p>Access Password: ${node.access_password}</p>

<p>
%if node.is_public == 1:
Public can post to node.
%else:
Public cannot post to node.
%endif
</p>

<p>
<%h:link href="${controller.path(action='edit', id=node.id)}" value="Edit" />
</p>