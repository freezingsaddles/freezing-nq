import json
import copy

from falcon import testing
import pytest

from freezing.nq.app import make_app
from freezing.nq.config import config
from freezing.nq.publish import ActivityPublisher, Destinations


def test_get_webhook(client):

    d = {'hub.challenge': 'asdf', 'hub.mode': 'mode', 'hub.verify_token': config.strava_verify_token}

    result = client.simulate_get('/webhook', params=d)
    print(result)
    assert result.json == {'hub.challenge': 'asdf'}


def test_get_webhook_bad_token(client):

    d = {'hub.challenge': 'asdf', 'hub.mode': 'mode', 'hub.verify_token': 'wrong'}

    with pytest.raises(AssertionError):
        result = client.simulate_get('/webhook', params=d)


def test_post_webhook(client, publisher:ActivityPublisher):

    d = dict(
        subscription_id=111,
        owner_id=222,
        object_type='activity',
        object_id=999,
        aspect_type='update',
        updates={'title': 'Hello world.'},
        event_time=1358919359,
    )

    result = client.simulate_post('/webhook', body=json.dumps(d), headers={'content-type': 'application/json'})

    called_with = copy.copy(d)
    called_with['event_time'] = '2013-01-23T05:35:59+00:00'

    publisher.publish_message.assert_called_with(called_with, dest=Destinations.activity_updated)


def test_post_webhook_noop(client, publisher:ActivityPublisher):

    d = dict(
        subscription_id=111,
        owner_id=222,
        object_type='gear',
        object_id=999,
        aspect_type='update',
        updates={},
        event_time=1358919359,
    )

    client.simulate_post('/webhook', body=json.dumps(d), headers={'content-type': 'application/json'})
 
    publisher.publish_message.assert_not_called()