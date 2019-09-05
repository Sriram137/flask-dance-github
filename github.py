import os
from github import Github
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/hello")
def index():
    return "/hello"


@app.route("/")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    access_token = access_token
    gh = Github(access_token)

    assert resp.ok
    return str(dir(github))
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

# def get_prs():
