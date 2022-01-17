from flask import Blueprint

userbp = Blueprint("userbp", __name__)


@userbp.route("/")
def index():
    return "This is an example app"
