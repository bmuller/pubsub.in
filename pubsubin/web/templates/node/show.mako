<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Node: ${node.name}</h3>
<%h:link href="${controller.path(action='addmessage', id=node.id)}" value="Post Message" />
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

<h4>Messages</h4>
%if len(msgs) == 0:
No messages yet.  <%h:link href="${controller.path(action='addmessage', id=node.id)}" value="Post one." />
%else:

<table><thead><td>Title</td><td>Sent</td></thead>
%for msg in msgs:
<td><%h:link href="${controller.path(action='viewmsg', id=msg.id)}" value="${msg.title}" /></td><td>${msg.created}</td>
%endfor
</table>

%endif