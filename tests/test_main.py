from flask_dance.consumer.storage import MemoryStorage
from githubclient import create_app


def acess_app(monkeypatch, authorize):
    if authorize:
        storage = MemoryStorage({"access_token": "fake-token"})
    else:
        storage = MemoryStorage()
    app = create_app()
    github_bp = app.blueprints["github"]
    monkeypatch.setattr(github_bp, "storage", storage)
    return app


def test_index_page(monkeypatch):
    app = acess_app(monkeypatch, False)
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Github Client" in response.data


def test_logout(monkeypatch):
    app = acess_app(monkeypatch, True)
    with app.test_client() as client:
        response = client.get("/logout")
        assert response.status_code == 302
        text = response.get_data(as_text=True)
        assert b"Redirecting..." in response.data


def test_github_authorized(monkeypatch):
    app = acess_app(monkeypatch, True)
    with app.test_client() as client:
        response = client.get("/github_authorized")
        assert response.status_code == 200
        text = response.get_data(as_text=True)


# TODO: test_main_utils_sincronize
# TODO: test_utils_get_user_data
