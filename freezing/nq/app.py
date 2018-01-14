from wsgiref import simple_server

import falcon

from freezing.nq.api.webhook import WebhookResource
from freezing.nq.middleware import RequireJSON


def make_app() -> falcon.API:
    # Configure your WSGI server to load "things.app" (app is a WSGI callable)
    app = falcon.API(middleware=[
        RequireJSON(),
    ])

    app.add_route('/webhook', WebhookResource())

    return app


# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, make_app())
    httpd.serve_forever()