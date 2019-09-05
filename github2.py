import os
from github import Github
from flask import Flask, redirect, url_for
import flask_dance.contrib.github
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = flask_dance.contrib.github.make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/hello")
def index():
    return "/hello"


@app.route("/")
def login():
    if not flask_dance.contrib.github.github.authorized:
        return redirect(url_for("github.login"))
    resp = flask_dance.contrib.github.github.get("/user")
    access_token = flask_dance.contrib.github.github.access_token

    # return str(access_token)

    # return str(flask_dance.contrib.github.github.token)

    gh = Github(access_token)
    org = gh.get_organization("Rippling")

    # return str(org)
    # repos = org.get_repos()

    repo = org.get_repo(name="rippling-main")

    prs = repo.get_pulls(state="OPEN")

    data = []

    for pr in prs:
        data.append({
            "message": pr.title,
            "link": pr.url,
            "name": pr.user.name,
        })
        return str(pr)

    return data

    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

# def get_prs():
