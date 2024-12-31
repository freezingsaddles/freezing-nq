import json
from typing import Any

import greenstalk
from freezing.model.msg.mq import DefinedTubes

from freezing.nq.autolog import log
from freezing.nq.config import config


class ActivityPublisher:
    """
    Abstraction for publishing an activity to a queue.

    (Currently uses beanstalkd, but that may change.  May also switch to using threads & queues to speed up.)
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def serialize_message(self, message) -> str:
        if isinstance(message, str):
            return message
        else:
            return json.dumps(message)

    def publish_message(self, message: Any, dest: DefinedTubes):
        """
        Publish the json-serializable message object (e.g. dict) to configured destination (e.g. queue, tube).

        :param message: A message object that can be serialized with json.dumps()
        """
        queue = greenstalk.Client((self.host, self.port), use=dest.value)
        try:
            queue.put(self.serialize_message(message))
        except Exception as ex:
            log.exception(f"Error publishing message: {ex}")
        finally:
            queue.close()


def configured_publisher() -> ActivityPublisher:
    return ActivityPublisher(host=config.BEANSTALKD_HOST, port=config.BEANSTALKD_PORT)
