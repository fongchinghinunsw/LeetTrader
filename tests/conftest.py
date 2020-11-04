""" Create test fixtures """

import os
import tempfile

import pytest
from leettrader import create_app
from utils import init_db


@pytest.fixture
def client():
    """ This client fixture will be called by each individual test """
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()

        print("yield the client")
        yield client

@pytest.fixture
def app():
  yield app