from flask import Flask
from flask_bootstrap import Bootstrap
import web.views.index

# default configuration
DATABASE = '/tmp/database/hydro.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'nimda'
PORT = 5060
HOST = "0.0.0.0"


class HydroWebServer():
    def __init__(self, crop_id):
        print("Initializing web server")
        self.svr = Flask(__name__)
        self.crop_id = crop_id
        # If HYDRO_SETTINGS environment value points to a config file
        # override the default configuration
        self.svr.config.from_envvar('HYDRO_SETTINGS', silent=True)
        Bootstrap(self.svr)
        self.svr.route('/', methods=['GET'])(web.views.index.index)

    def start(self, debug=False):
        print("Starting web server")
        self.svr.run(host=HOST, port=PORT, debug=debug)


def run_webserver(crop_id):
    server = HydroWebServer(crop_id)
    server.start()
