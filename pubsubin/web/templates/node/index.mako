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
  <tr><td><a href="${controller.path(node, id=node.id)}">${node.name}</a></td></tr>
 % endfor
</table>
</p>
% endif