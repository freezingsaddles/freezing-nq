import logging
from envparse import Env

# Is this really adding any value?
env = Env(
    DEBUG=bool,
    STRAVA_VERIFY_TOKEN=str,
    BEANSTALKD_SERVER=str,
)

class Config:
    debug = env('DEBUG', default=False)  # type: bool
    strava_verify_token = env('STRAVA_VERIFY_TOKEN', default='STRAVA')
    beanstalkd_server = env('BEANSTALKD_SERVER', default='beanstalkd.container')

config = Config()


def init_logging():
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
