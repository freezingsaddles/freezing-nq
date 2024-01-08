import falcon


class HealthResource:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        Just an arbitrary response for now.
        """
        resp.media = {"status": "Server is happy."}
