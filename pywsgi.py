# Patch low-level libraries
from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
# Import app
from start import app

WSGIServer((
    "0.0.0.0", # str(HOST)
    5000,  # int(PORT)
), app.wsgi_app, handler_class=WebSocketHandler).serve_forever()
