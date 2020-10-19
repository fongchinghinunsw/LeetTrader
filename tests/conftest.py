""" Create test fixtures """

import os
import tempfile

import pytest
from leettrader import create_app
from run import app
from utils import init_db


@pytest.fixture
def client():
    """ This client fixture will be called by each individual test """
    # returns a low-level file handle and a random file name
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    # disable error catching during request handling, so that you get
    # better error reports when performing test requests against the application.
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()

        print("yield the client")
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])