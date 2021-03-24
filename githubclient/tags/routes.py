import json
import os

from dotenv import load_dotenv
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_dance.contrib.github import github
from githubclient import db
from githubclient.models import Repository, Tags
from githubclient.tags.forms import TagsForm
from githubclient.utils import get_user_data

load_dotenv()


tags = Blueprint("tags", "__name__")


@tags.context_processor
def github_authorized():
    return {"github_authorized": github.authorized}


@tags.route("/tags", methods=["GET"])
def list():
    if not github.authorized:
        return redirect(url_for("github.login"))
    github_account_info = get_user_data()

    page = request.args.get("page", 1, type=int)
    rows_per_page = int(os.getenv("ROWS_PER_PAGE"))

    tags = []
    if github_account_info and "id" in github_account_info:
        tags = (
            Tags.query.filter_by(id_github_account=github_account_info["id"])
            .order_by(Tags.name.asc())
            .paginate(page=page, per_page=rows_per_page)
        )

    return render_template("tags.html", current_page="tags", tags=tags)


@tags.route("/tags/add", methods=["GET", "POST"])
def add():
    if not github.authorized:
        return redirect(url_for("github.login"))
    github_account_info = get_user_data()

    form = TagsForm()
    if form.validate_on_submit():
        if request.form.get("id_github_account"):
            id_github_account = form.id_github_account.data
        else:
            id_github_account = github_account_info["id"]
        data = Tags(name=form.name.data, id_github_account=id_github_account)
        db.session.add(data)
        db.session.commit()
        flash("A tag foi criada com sucesso!", "success")
        return redirect(url_for("tags.list"))

    return render_template("tags_create.html", form=form, legend="Nova tag")


@tags.route("/tags/edit/<int:tag_id>", methods=["GET", "POST"])
def edit(tag_id):
    if not github.authorized:
        return redirect(url_for("github.login"))
    github_account_info = get_user_data()

    tag = Tags.query.filter_by(
        id=tag_id, id_github_account=github_account_info["id"]
    ).first_or_404()
    form = TagsForm()
    form.origin_name.data = tag.name
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.commit()
        flash("A tag foi atualizada com sucesso!", "success")
        return redirect(url_for("tags.list"))
    elif request.method == "GET":
        form.name.data = tag.name
    return render_template(
        "tags_create.html", form=form, title=tag.name, tag=tag, legend="Edição da tag"
    )


@tags.route("/tags/delete", methods=["POST"])
def delete():
    if not github.authorized:
        return redirect(url_for("github.login"))
    github_account_info = get_user_data()

    tag_id = request.form.get("tag_id")
    if request.form.get("id_github_account"):
        id_github_account = request.form.get("id_github_account")
    else:
        id_github_account = github_account_info["id"]

    tag = Tags.query.filter_by(
        id=tag_id, id_github_account=id_github_account
    ).first_or_404()
    db.session.delete(tag)
    db.session.commit()

    flash("A tag foi excluída com sucesso!", "success")
    return redirect(url_for("tags.list"))


@tags.route("/tags/getTags", methods=["GET"])
def getTags():
    if not github.authorized:
        return redirect(url_for("github.login"))
    github_account_info = get_user_data()

    if "id" in github_account_info:
        id_github_account = github_account_info["id"]
    else:
        id_github_account = request.form.get("id_github_account")

    tags_info = {}
    tags = (
        Tags.query.filter_by(id_github_account=id_github_account)
        .order_by(Tags.name.asc())
        .all()
    )

    for tag in tags:
        tags_info[tag.id] = tag.name

    return json.dumps(tags_info)


@tags.route("/tags/relationship", methods=["POST"])
def relationship():
    if not github.authorized:
        return redirect(url_for("github.login"))

    github_project_id = request.form.get("github_project_id")
    repository = Repository.query.filter_by(id_repo=github_project_id).first_or_404()

    tags = request.form.getlist("tags")
    for tag_id in tags:
        tag = Tags.query.filter_by(id=tag_id).first_or_404()

        if tag not in repository.tags:
            repository = Repository.query.filter_by(
                id_repo=github_project_id
            ).first_or_404()
            repository.tags.append(tag)
            db.session.commit()

    flash("A tag foi relacionada com sucesso!", "success")
    return redirect(url_for("main.home"))


@tags.route("/tags/removeRelationship", methods=["POST"])
def removeRelationship():
    if not github.authorized:
        return redirect(url_for("github.login"))

    repository_id = request.form.get("repository_id")
    repository = Repository.query.filter_by(id_repo=repository_id).first_or_404()
    tag_id = request.form.get("tag_id")
    tag = Tags.query.filter_by(id=tag_id).first_or_404()

    repository.tags.remove(tag)
    db.session.commit()

    flash("A tag foi removida com sucesso!", "success")
    return redirect(url_for("main.home"))
