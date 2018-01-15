import logging
from envparse import env

# Is this really adding any value?
# env = Env(
#     DEBUG=bool,
#     STRAVA_VERIFY_TOKEN=str,
#     BEANSTALKD_HOST=str,
# )

class Config:
    debug = env('DEBUG', default=False)  # type: bool
    strava_verify_token = env('STRAVA_VERIFY_TOKEN', default='STRAVA')
    beanstalkd_host = env('BEANSTALKD_HOST', default='beanstalkd.container')
    beanstalkd_port = env('BEANSTALKD_PORT', cast=int, default=11300)

config = Config()


def init_logging():
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
