import json
import requests
from flask_dance.consumer.storage import MemoryStorage
from githubclient import create_app
from flask import url_for
from random import randrange
from githubclient.main.routes import *

def acess_app(monkeypatch, authorize):
    if (authorize):
        storage = MemoryStorage({"access_token": "fake-token"})
    else:
        storage = MemoryStorage()
    app = create_app()
    github_bp = app.blueprints['github']
    monkeypatch.setattr(github_bp, "storage", storage)
    return app

def get_random_num():
    return str(randrange(10000))

def test_index_page(monkeypatch):
    app = acess_app(monkeypatch, False)
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Github Client' in response.data

def test_logout(monkeypatch):
    app = acess_app(monkeypatch, True)
    with app.test_client() as client:
        response = client.get("/logout")
        assert response.status_code == 302
        text = response.get_data(as_text=True)
        assert b'Redirecting...' in response.data

# TODO: test_main_github_authorized
# TODO: test_main_utils_sincronize
# TODO: test_utils_get_user_data