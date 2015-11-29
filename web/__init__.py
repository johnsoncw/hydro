from flask import Flask

print("Loading web server")

# default configuration
DATABASE = '/tmp/database/hydro.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'nimda'

web_server = Flask(__name__)
