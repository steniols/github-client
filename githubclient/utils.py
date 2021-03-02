import json
from flask_dance.contrib.github import make_github_blueprint, github


def get_user_data():
    github_account_info = github.get('/user')
    github_account_info_json = json.dumps({})
    if github_account_info.ok:
        github_account_info_json = github_account_info.json()
    return github_account_info_json
