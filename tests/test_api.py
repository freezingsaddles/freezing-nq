import json

import arrow
from freezing.model.msg.mq import ActivityUpdate, DefinedTubes
from freezing.model.msg.strava import AspectType

from freezing.nq.config import config
from freezing.nq.publish import ActivityPublisher


def test_get_webhook(client):
    d = {
        "hub.challenge": "asdf",
        "hub.mode": "mode",
        "hub.verify_token": config.STRAVA_VERIFY_TOKEN,
    }

    result = client.simulate_get("/webhook", params=d)
    print(result)
    assert result.json == {"hub.challenge": "asdf"}


def test_get_webhook_bad_token(client):
    d = {"hub.challenge": "asdf", "hub.mode": "mode", "hub.verify_token": "wrong"}

    result = client.simulate_get("/webhook", params=d)
    assert result.status_code == 403


def test_post_webhook(client, publisher: ActivityPublisher):
    d = dict(
        subscription_id=111,
        owner_id=222,
        object_type="activity",
        object_id=999,
        aspect_type="update",
        updates={"title": "Hello world."},
        event_time=1358919359,
    )

    result = client.simulate_post(
        "/webhook", body=json.dumps(d), headers={"content-type": "application/json"}
    )
    assert result.status_code == 200

    message = ActivityUpdate()
    message.athlete_id = d["owner_id"]
    message.event_time = arrow.get(d["event_time"]).datetime
    message.activity_id = d["object_id"]
    message.operation = AspectType(d["aspect_type"])
    message.updates = d["updates"]

    called_with = dict(
        activity_id=d["object_id"],
        athlete_id=d["owner_id"],
        operation=d["aspect_type"],
        event_time="2013-01-23T05:35:59+00:00",
        updates=d["updates"],
    )

    publisher.publish_message.assert_called_with(
        called_with, dest=DefinedTubes.activity_update
    )
