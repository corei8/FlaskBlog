from core.microsite_utils.globals import HTML


def build_default_home():
	with open(HTML+'home.html', 'w') as f:
		f.write(
				"""
<!DOCTYPE html>
<html>
<head>
<style>
.main_container {
  display: flex;
  flex-direction: column;
 height: 98vh;
  width: 100%;
  font-family: sans-serif;
  justify-content: space-evenly;
  align-items: center;
}

.welcom_link {
  height: 15vh;
  width: 50vw;
  display: flex;
  flex-direction: column;
    justify-content: space-between;
  align-items: center;
  /*border: solid 1px black;*/
  border-radius: 1em;
  padding: 5em;
  box-shadow: 10px 10px 28px -2px rgba(0,0,0,0.75);
-webkit-box-shadow: 10px 10px 28px -2px rgba(0,0,0,0.75);
-moz-box-shadow: 10px 10px 28px -2px rgba(0,0,0,0.75);
}

.title {
    font-size: 56pt;
}

.explanation {
  font-size: 25pt;
}

.login {
  color: black;
  text-decoration: none;
}

.login:hover {
  color: blue;
}

.footer::before {
  content: "You are running Microsite v. "
}
</style>
</head>
<body>
<div class="main_container">
  <span class="title">MicroSite</span>
  <div class="welcom_link">
    <span class="explanation">You have successfully installed MicroSite!</span>
    <a href="{{ url_for('login') }}" class="login">Get Started</a>
  </div>
  <footer class="footer">0.0.1</footer>
</div>
</body>
</html>
				"""
				)
	return None
