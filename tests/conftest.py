import json

import pytest
import pytest_mock
from falcon import testing

from freezing.nq.app import make_app
from freezing.nq.config import config
from freezing.nq.publish import ActivityPublisher


@pytest.fixture()
def publisher(mocker):
    return mocker.Mock(spec=ActivityPublisher)


@pytest.fixture()
def client(publisher):
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(make_app(publisher=publisher))
