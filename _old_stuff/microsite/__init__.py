import os
from flask import Flask

def create_app(test_config='Development'):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object('config.'+test_config)

	return app

# import microsite.routes
