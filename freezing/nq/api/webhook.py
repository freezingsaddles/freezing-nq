import falcon

from stravalib import Client
from freezing.nq.config import config
from freezing.nq.autolog import log


class WebhookResource:

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        The GET request is used by Strava, when the webhook is initially registered, to validate the API.
        """
        client = Client()

        strava_request = {k: req.get_param(k) for k in ('hub.challenge', 'hub.mode', 'hub.verify_token')}

        challenge_response = client.handle_subscription_callback(strava_request,
                                                                 verify_token=config.strava_verify_token)

        resp.media = challenge_response

    def on_post(self, req: falcon.Request, resp: falcon.Response):

        client = Client()
        result = client.handle_subscription_update(req.media)
        log.info(result.to_dict())
        """
        subscription_id = Attribute(six.text_type)
        owner_id = Attribute(six.text_type)
        object_id = Attribute(six.text_type)
        object_type = Attribute(six.text_type)
        aspect_type = Attribute(six.text_type)
        event_time = TimestampAttribute()
        """