<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Node: ${node.name}</h3>
<p>Shortname: ${node.shortname | h}</p>
<p>Description: ${node.description | h}</p>

<p>
<%h:link href="${controller.path(action='edit', id=node.id)}" value="Edit" />
</p>