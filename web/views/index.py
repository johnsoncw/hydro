from web import web_server


@web_server.route('/')
def index():
    return 'Hello World!'

