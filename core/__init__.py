from flask import Flask

app = Flask(__name__)

# ! 'from core import routes' must be at the end!!
from core import routes
