# Freezing Saddles Enqueue

This component is part of the [Freezing Saddles](http://freezingsaddles.com) project.  Its purpose is to receive [webhook activity events from Strava](http://strava.github.io/api/partner/v3/events/) and queue them up for processing. 

It is designed to run as a container and should be configured with environment variables for:
- `BEANSTALKD_HOST`: The hostname (probably a container link) to a beanstalkd server.
- `BEANSTALKD_PORT`: The port for beanstalkd server (default 11300)
- `STRAVA_VERIFY_TOKEN`: The token to use when verifying the Strava challenge response (must match token used to register subscription).