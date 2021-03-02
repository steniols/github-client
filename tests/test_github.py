# from flask_dance.consumer.storage import MemoryStorage
# from githubclient import create_app



# @main.route("/teste_login")
# def teste_login():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     return "You are authorized"

# def acess_app(monkeypatch, authorize):
#     if (authorize):
#         storage = MemoryStorage({"access_token": "fake-token"})
#     else:
#         storage = MemoryStorage()
#     app = create_app()
#     github_bp = app.blueprints['github']
#     monkeypatch.setattr(github_bp, "storage", storage)
#     return app


# def test_index_unauthorized(monkeypatch):
#     app = acess_app(monkeypatch, False)
    
#     with app.test_client() as client:
#         response = client.get("/teste_login", base_url="https://example.com/")

#     assert response.status_code == 302
#     assert response.headers["Location"] == "https://example.com/github_login/github"

# def test_index_authorized(monkeypatch):
#     app = acess_app(monkeypatch, True)

#     with app.test_client() as client:
#         response = client.get("/teste_login", base_url="https://example.com")

#     assert response.status_code == 200
#     text = response.get_data(as_text=True)
#     assert text == "You are authorized"