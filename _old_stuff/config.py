from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Development:

	FLASK_ENV = 'development'
	TEMPLATES_FOLDER = 'templates'
	SECRET_KEY=environ.get('SECRET_KEY')
	# DATABASE=path.join(app.instance_path, 'microsite.sqlite')
	FLASK_APP='microsite'
	TESTING = True
	DEBUG = True
