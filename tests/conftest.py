import pytest

from flask import current_app
from githubclient import create_app
from flask_dance.contrib.github import github

@pytest.fixture
def app():
    app = current_app()
    return app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def flask_dance_sessions():
    return github