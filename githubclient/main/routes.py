
import os
import json
import requests
from flask import render_template, request, Blueprint, redirect, url_for, session, current_app
from flask_dance.contrib.github import make_github_blueprint, github
from githubclient import db, bcrypt
from githubclient.main.forms import SearchForm
from githubclient.models import Repository, Tags
from githubclient.main.utils import *
from sqlalchemy import or_, and_
from dotenv import load_dotenv
load_dotenv()


main = Blueprint('main', '__name__')


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    repositories = None
    github_account_info = None
    github_account_info_json = None
    search_form = SearchForm()
    if github.authorized:
        page = request.args.get('page', 1, type=int)
        rows_per_page = int(os.getenv('ROWS_PER_PAGE'))
        github_account_info = github.get('/user')

        if github_account_info.ok:
            sincronize_repositories()
            github_account_info_json = github_account_info.json()

            if search_form.validate_on_submit():
                search_term = search_form.search.data
                search = "%{}%".format(search_term)
                repositories = (
                    db.session.query(Repository)
                        .join(Repository.tags, isouter=True)
                        .filter(
                            or_(
                                Repository.name.like(search),
                                Repository.description.like(search),
                                Tags.name.like(search)
                            ),
                            and_(Repository.id_github_account.like(github_account_info_json['id']))
                        ).group_by(Repository.id)
                    ).paginate(page=page)
            else:
                repositories = Repository.query.filter_by(id_github_account=github_account_info_json['id']).order_by(Repository.stars.desc()).paginate(page=page, per_page=rows_per_page) 

    return render_template(
        'home.html', 
        current_page="home", 
        repositories=repositories,
        github=github,
        github_account_info=github_account_info_json,
        search_form=search_form
    )


@main.route("/logout")
def logout():
    blueprint = current_app.blueprints['github']
    access_token = blueprint.token.get('access_token')
    if access_token:
        client_id = blueprint.client_id
        client_secret = blueprint.client_secret

        headers = {'Accept': 'application/vnd.github.v3+json'}
        data = '{"access_token":"' + access_token + '"}'
        response = github.delete(
            'https://api.github.com/applications/{}/grant'.format(client_id), 
            headers=headers,
            data=data,
            auth=(client_id, client_secret)
        )
        return redirect(url_for('main.home'))


@main.context_processor
def github_authorized():
    github_account_info = github.get('/user')
    return {'github_authorized':github_account_info.ok}