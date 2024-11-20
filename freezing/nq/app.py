from wsgiref import simple_server

import falcon

from freezing.nq.api.health import HealthResource
from freezing.nq.api.webhook import WebhookResource
from freezing.nq.publish import ActivityPublisher, configured_publisher


class RequireJSON:
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                "This API only supports responses encoded as JSON.",
                href="http://docs.examples.com/api/json",
            )

        if req.method in ("POST", "PUT"):
            if "application/json" not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    "This API only supports requests encoded as JSON.",
                    href="http://docs.examples.com/api/json",
                )


def make_app(publisher: ActivityPublisher = None) -> falcon.API:
    """
    Builds the WSGI application we'll be serving.
    """
    if publisher is None:
        publisher = configured_publisher()

    app = falcon.API(
        middleware=[
            RequireJSON(),
        ]
    )

    app.add_route("/health", HealthResource())
    app.add_route("/webhook", WebhookResource(publisher=publisher))

    return app


# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8000, make_app())
    httpd.serve_forever()
