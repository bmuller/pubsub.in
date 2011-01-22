<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Node: ${node.name}</h3>
<%h:link href="${controller.path(action='addmessage', id=node.id)}" value="Post Message" /><br />
<%h:link href="${controller.path(controller='subscription', action='add', node_id=node.id)}" value="Subscribe To Node" />
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
<p>
%if len(msgs) == 0:
No messages yet.  <%h:link href="${controller.path(action='addmessage', id=node.id)}" value="Post one." />
%else:

<table><thead><td>Title</td><td>Sent</td></thead>
%for msg in msgs:
<tr>
<td><%h:link href="${controller.path(action='viewmsg', id=msg.id)}" value="${msg.title}" /></td><td>${msg.created}</td>
</tr>
%endfor
</table>
%endif
</p>

<h4>Subscriptions</h4>
<p>
%if len(subs) == 0:
No subscriptions yet.  <%h:link href="${controller.path(controller='subscription', action='add', node_id=node.id)}" value="Subscribe To Node" />
%else:

<table><thead><td>Subscription Type</td><td>Description</td><td></td><td></td></thead>
%for sub in subs:
<tr>
<td>${router.getSubtype(sub.type_name).name}</td><td>${router.getSubtype(sub.type_name).toString(sub)}</td>
<td><%h:link href="${controller.path(action='edit', id=sub.id, controller='subscription')}" value="edit" /></td>
<td><%h:link href="${controller.path(action='delete', id=sub.id, controller='subscription')}" value="delete" /></td>
</tr>
%endfor
</table>
%endif
</p>
