<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Add ${subtype.shortname} Subscription To &quot;${node.name}&quot;</h3>
${controller.include("subscriptionform")}
