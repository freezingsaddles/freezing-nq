import json
import falcon

from freezing.nq.autolog import log
from freezing.nq.config import config
from freezing.nq.publish import ActivityPublisher

from freezing.model.msg.strava import SubscriptionUpdate, SubscriptionUpdateSchema, SubscriptionCallbackSchema, \
    SubscriptionCallback, ObjectType
from freezing.model.msg.mq import DefinedTubes, ActivityUpdate, ActivityUpdateSchema


class WebhookResource:

    def __init__(self, publisher: ActivityPublisher):
        self.publisher = publisher

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        The GET request is used by Strava, when the webhook is initially registered, to validate this endpoint.

        See: http://strava.github.io/api/partner/v3/events/
        """

        strava_request = {k: req.get_param(k) for k in ('hub.challenge', 'hub.mode', 'hub.verify_token')}

        schema = SubscriptionCallbackSchema(strict=True)
        callback: SubscriptionCallback = schema.load(strava_request).data
        assert config.STRAVA_VERIFY_TOKEN == callback.hub_verify_token

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'hub.challenge': callback.hub_challenge})

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """
        Receives a POSt request from Strava to indicate that an activity has been created or updated.

        We use stravalib to deserialize this (although the structure is pretty trivial).  This will the be published to
        beanstalkd (etc.) for picking up by main processing component.

        Message payload:
                subscription_id = Attribute(six.text_type)
                owner_id = Attribute(six.text_type)
                object_id = Attribute(six.text_type)
                object_type = Attribute(six.text_type)
                aspect_type = Attribute(six.text_type)
                event_time = TimestampAttribute()

        See: http://strava.github.io/api/partner/v3/events/
        """

        schema = SubscriptionUpdateSchema(strict=True)
        result: SubscriptionUpdate = schema.load(req.media).data

        # We only care about activities
        if result.object_type is not ObjectType.activity:
            log.info("Ignoring non-activity webhook: {}".format(req.media))
        else:
            message = ActivityUpdate()
            message.athlete_id = result.owner_id
            message.event_time = result.event_time
            message.activity_id = result.object_id
            message.operation = result.aspect_type
            message.updates = result.updates

            json_data = ActivityUpdateSchema().dump(message).data

            log.info("Publishing activity-update: {}".format(message))
            self.publisher.publish_message(json_data,
                                           dest=DefinedTubes.activity_update)
