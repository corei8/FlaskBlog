from flask import Flask

application = Flask(__name__)

# ! 'from app import routes' must be at the end!!
from app import routes
