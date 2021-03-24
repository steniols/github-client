from flask_login import UserMixin

from githubclient import db

rel = db.Table(
    "rel",
    db.Column("id_tag", db.Integer, db.ForeignKey("tags.id")),
    db.Column("id_repo", db.Integer, db.ForeignKey("repository.id_repo")),
)


class Repository(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_repo = db.Column(db.Integer, unique=True, nullable=False)
    id_github_account = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=False)
    stars = db.Column(db.String(255), nullable=False)

    tags = db.relationship(
        "Tags", secondary=rel, backref=db.backref("tags", lazy="dynamic")
    )

    def __repr__(self):
        return f"Tags('{self.name}', '{self.id_repo}, '{self.id_github_account}')"


class Tags(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    id_github_account = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Tags('{self.name}', '{self.id_github_account}')"
