import logging
from envparse import Env

env = Env(
    DEBUG=bool,
    STRAVA_VERIFY_TOKEN=str,
    BEANSTALK_SERVER=str,
)

class Config:
    debug = env('DEBUG', default=False)  # type: bool
    strava_verify_token = env('STRAVA_VERIFY_TOKEN', default='STRAVA')
    beanstalk_server = env('BEANSTALK_SERVER', default='beanstalk.container')

config = Config()


def init_logging():
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
