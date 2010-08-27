<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Add Subscription To &quot;${node.name}&quot;</h3>
<p>
Enabled suscribers:
<ul>
%for subscriber in subscribers:
  <%h:link href="${controller.path(action='configure', id=node.id, subscriber_name=subscriber.shortname)}" value="${subscriber.name}" /><br />
  ${subscriber.description}
%endfor
</li>
</p>