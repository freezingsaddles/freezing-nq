import falcon

from stravalib import Client
from freezing.nq.config import config
from freezing.nq.autolog import log


class HealthResource:

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        Just an arbitrary response for now.
        """
        resp.media = {'status': 'Server is happy.'}