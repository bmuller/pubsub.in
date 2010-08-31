<%inherit file="layout.mako"/>
<%namespace module="twistler.htmlhelpers" name="h" />

<h3>Edit ${subscriber.shortname} Subscription</h3>
${controller.include("subscriptionform")}
