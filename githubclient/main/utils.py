from flask_dance.contrib.github import github
from githubclient import db
from githubclient.models import Repository
from githubclient.utils import get_user_data


def sincronize_repositories():
    github_account_info = get_user_data()
    repositories = github.get("/users/" + github_account_info["login"] + "/repos")

    for item in repositories.json():
        repo = Repository.query.filter_by(id_repo=item["id"]).first()
        if not repo:
            data = Repository(
                id_repo=item["id"],
                name=item["full_name"],
                id_github_account=github_account_info["id"],
                description=item["description"],
                url=item["svn_url"],
                stars=item["stargazers_count"],
            )
            db.session.add(data)
            db.session.commit()
