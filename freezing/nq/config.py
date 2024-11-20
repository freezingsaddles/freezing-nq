import logging
import os

from envparse import env

envfile = os.environ.get("APP_SETTINGS", os.path.join(os.getcwd(), ".env"))

if os.path.exists(envfile):
    env.read_envfile(envfile)


class Config:
    DEBUG: bool = env("DEBUG", default=False)
    STRAVA_VERIFY_TOKEN: str = env("STRAVA_VERIFY_TOKEN", default="STRAVA")
    BEANSTALKD_HOST: str = env("BEANSTALKD_HOST", default="127.0.0.1")
    BEANSTALKD_PORT: int = env("BEANSTALKD_PORT", cast=int, default=11300)


config = Config()


def init_logging():
    logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)
