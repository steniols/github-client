import os, random
from flask_dance.consumer.storage import MemoryStorage
from githubclient import create_app
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname('../githubclient/.env'))
load_dotenv(os.path.join(BASEDIR, '.env'))

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
    return str(random.random())

def test_tags_list(monkeypatch):
    app = acess_app(monkeypatch, True)

    with app.test_client() as client:
        response = client.get("/tags")
        assert response.status_code == 200
        text = response.get_data(as_text=True)
        assert b'Todas as tags' in response.data

def test_tags_add(monkeypatch):
    app = acess_app(monkeypatch, True)

    with app.test_client() as client:
        response = client.get("/tags/add")
        assert response.status_code == 200
        text = response.get_data(as_text=True)
        assert b'Nova tag' in response.data

def test_tags_add_post(monkeypatch):
    app = acess_app(monkeypatch, True)

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'name':'Front-end','id_github_account':get_random_num()}

    with app.test_client() as client:
        response = client.post(os.getenv('BASE_URL') + '/tags/add',headers=headers,data=payload)
        assert response.status_code == 200

def test_tags_edit(monkeypatch):
    app = acess_app(monkeypatch, True)

    with app.test_client() as client:
        response = client.get("/tags/edit/a")
        assert response.status_code == 404
        text = response.get_data(as_text=True)
        assert b'404' in response.data

def test_tags_delete_post(monkeypatch):
    app = acess_app(monkeypatch, True)

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'tag_id':get_random_num(),'id_github_account':str(random.random())}

    with app.test_client() as client:
        response = client.post(os.getenv('BASE_URL') + '/tags/delete',headers=headers,data=payload)
        assert response.status_code == 404

def test_get_tags(monkeypatch):
    app = acess_app(monkeypatch, True)

    with app.test_client() as client:
        response = client.get("/tags/getTags?id_github_account=" + get_random_num())
        assert response.status_code == 200
        text = response.get_data(as_text=True)
        assert b'{}' in response.data

def test_relationship(monkeypatch):
    app = acess_app(monkeypatch, True)

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'github_project_id':get_random_num(),'tags':'{}'}

    with app.test_client() as client:
        response = client.post(os.getenv('BASE_URL') + '/tags/relationship',headers=headers,data=payload)
        assert response.status_code == 404

def test_remove_relationship(monkeypatch):
    app = acess_app(monkeypatch, True)

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'tag_id':get_random_num(),'repository_id':get_random_num()}

    with app.test_client() as client:
        response = client.post(os.getenv('BASE_URL') + '/tags/removeRelationship',headers=headers,data=payload)
        assert response.status_code == 404
