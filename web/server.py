from web import web_server
import web.views.index

# If HYDRO_SETTINGS environment value points to a config file
# override the default configuration
web_server.config.from_envvar('HYDRO_SETTINGS', silent=True)


def start():
    print("Starting web server")
    web_server.run(host="0.0.0.0", port=5090, debug=True)
