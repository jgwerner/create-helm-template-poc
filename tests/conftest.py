import logging

import pytest
from templategenerator import create_app
from templategenerator.templategenerator import HelmTemplateGenerator


@pytest.fixture(scope="session")
def api():
    """Create application for the tests."""
    api = create_app()
    api.logger.setLevel(logging.CRITICAL)
    ctx = api.test_request_context()
    ctx.push()

    api.config["TESTING"] = True
    api.testing = True

    yield api
    ctx.pop()


@pytest.fixture(scope="session")
def client(api):
    client = api.test_client()

    # Establish an application context before running the tests.
    ctx = api.app_context()
    ctx.push()

    yield client
    ctx.pop()
