<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Nodes</h3>
<p><%h:link href="${controller.path('create')}" value="Create a node" /></p>

% if len(nodes) == 0:
<p>No nodes.</p>
% endif

% if len(nodes) > 0:
<p>
<table>
 <thead><td>Name</td></thead>
 % for node in nodes:
  <tr><td><%h:link href="${controller.path('show', id=node.id)}" value="${node.name}" /></td></tr>
 % endfor
</table>
</p>
% endif