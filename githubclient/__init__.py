import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from githubclient.config import Config
from flask_dance.contrib.github import make_github_blueprint, github

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from githubclient.main.routes import main
    from githubclient.tags.routes import tags
    from githubclient.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(tags)
    app.register_blueprint(errors)


    github_blueprint = make_github_blueprint(client_id='34c2485e8a5d1d5d69be',
                                            client_secret='a33fb8e966f5b7d13e7cd5b01c5db454ccd21f94')

    app.register_blueprint(github_blueprint, url_prefix='/github_login')

    with app.app_context():
        db.create_all()

    return app