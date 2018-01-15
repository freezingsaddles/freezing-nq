import enum
import json
from typing import Any

from contextlib import closing

import greenstalk

from freezing.nq.config import config
from freezing.nq.autolog import log


class Destinations(enum.Enum):
    activity_created = 'new-activities'
    activity_updated = 'updated-activities'


class ActivityPublisher:
    """
    Abstraction for publishing an activity to a queue.

    (Currently uses beanstalkd, but that may change.  May also switch to using threads & queues to speed up.)
    """

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

    def serialize_message(self, message) -> str:
        if isinstance(message, str):
            return message
        else:
            return json.dumps(message)

    def publish_message(self, message:Any, dest:Destinations):
        """
        Publish the json-serializable message object (e.g. dict) to configured destination (e.g. queue, tube).

        :param message: A message object that can be serialized with json.dumps()
        """
        queue = greenstalk.Client(host=self.host, port=self.port, use=dest.value)
        try:
            queue.put(self.serialize_message(message))
        except:
            log.exception("Error publishing message.")
        finally:
            queue.close()


def configured_publisher() -> ActivityPublisher:
    return ActivityPublisher(host=config.beanstalkd_host, port=config.beanstalkd_port)