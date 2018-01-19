import logging
from envparse import Env

env = Env(
    DEBUG=dict(cast=bool, default=False),
    STRAVA_VERIFY_TOKEN=dict(cast=str, default='STRAVA'),
    BEANSTALKD_HOST=dict(cast=str, default='beanstalkd.container'),
    BEANSTALKD_PORT=dict(cast=int, default=11300)
)


class Config:
    debug = env('DEBUG')  # type: bool
    strava_verify_token = env('STRAVA_VERIFY_TOKEN')
    beanstalkd_host = env('BEANSTALKD_HOST')
    beanstalkd_port = env('BEANSTALKD_PORT')

config = Config()


def init_logging():
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
