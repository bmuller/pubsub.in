<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <!-- design modified from http://www.oswd.org/design/preview/id/3621 -->
  <meta http-equiv="Content-Type" content="text/html; charset=us-ascii" />
  <title>PubSub.in: A PubSubHub</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css" />
</head>
<body>
  <div id="container">
    <div id="header">
      <h1>PubSubin'</h1>
      <h2>a pub sub hub, bub</h2><br />
      <hr />
    </div>

    <div id="left">
      % for mname, mitems in menu.items():
        <h3>${mname}</h3>
        <ul>
        % for (name, url) in mitems:
          <li>&raquo; <a href="${url}">${name}</a></li>
        % endfor
        </ul>
      % endfor
    </div>

    <div id="main">
      % if message != "":
      <div id="message">${message}</div>
      % endif
      ${self.body()}
    </div>
    <div id="footer">
      <hr />
      <p class="left"></p>
      <p class="right">this project is open source</p>
      <p>&nbsp;</p>
    </div>
  </div>
</body>
</html>
