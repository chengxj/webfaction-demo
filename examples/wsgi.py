#Command to run uWSGI : uwsgi --http :8000 --gevent 100 --http-websockets --module wsgi
#Commands for separate instances: 
#uwsgi  --socket 8001 --buffer-size=32768 --workers=5 --master --module wsgi_django
#uwsgi  --http-socket 9001 --gevent 1000 --http-websockets --workers=2 --master --module wsgi_websocket

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatserver.settings')
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer

_django_app = get_wsgi_application()
_websocket_app = uWSGIWebsocketServer()

def application(environ, start_response):
    if environ.get('PATH_INFO').startswith(settings.WEBSOCKET_URL):
        return _websocket_app(environ, start_response)
    return _django_app(environ, start_response)

