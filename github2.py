import os
from github import Github
from flask import Flask, redirect, url_for
import flask_dance.contrib.github
from flask_dance.contrib.github import make_github_blueprint, github
from collections import defaultdict
from itertools import chain

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = flask_dance.contrib.github.make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")

followListMap = {
    "insurance": ["VishalRocks", "vampire-slayer", "chenlwilson", "shridharama", "simrandokania1995", "Sriram137", "Equlnox", "richa1995", "therealsanmah", "DefCon-007", "architrai175"]
}


@app.route("/hello")
def index():
    return "/hello"


@app.route("/<follow>")
def login(follow=None):
    if not flask_dance.contrib.github.github.authorized:
        return redirect(url_for("github.login"))
    access_token = flask_dance.contrib.github.github.access_token
    gh = Github(access_token)
    org = gh.get_organization("Rippling")

    if follow and not followListMap.get(follow):
        return "Follow string not found. Add to followListMap"

    repo_names = ["rippling-main", "rippling-webapp"]
    repo_prs = []

    for repo_name in repo_names:
        repo = org.get_repo(name=repo_name)
        prs = repo.get_pulls(state="OPEN")

        repo_prs.append((repo_name, prs))
    nameMap = defaultdict(lambda: defaultdict(list))

    for repo_pr in repo_prs:
        repoName, prs = repo_pr
        for pr in prs:
            if follow:
                followList = followListMap[follow]
                if str(pr.user.name) not in followList:
                    continue
            nameMap[pr.user.login][repoName].append({
                "message": pr.title,
                "link": pr.html_url,
            })

    text = ""
    for key in nameMap:
        text += "<ul>"
        text += "<li> %s </li>" % key
        for repoName in nameMap[key]:
            text += "<ul>"
            text += "<h5> %s </h5>" % repoName
            for data in nameMap[key][repoName]:
                text += '<li><a href="%s">%s</a></li>' % (data["link"], data["message"])
            text += "</ul>"
        text += "</ul>"
        text += "<br />"

    return text
