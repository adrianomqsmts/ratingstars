"""View de controle de requisições de error da aplicação como 404 e 500."""
from flask import Blueprint, Response, render_template

from project.configs.server import server

errorsbp = Blueprint("errors", __name__)


@errorsbp.app_errorhandler(404)
def handle_404(err) -> Response:
    """Page not found.

    Args:
        e (_type_): error

    Returns:
        Response: template, 404
    """
    return render_template("error/404.html"), 404


@errorsbp.app_errorhandler(500)
def handle_500(err):
    """Error on server.

    Args:
        e (_type_): error

    Returns:
        Response: template, 500
    """
    return render_template("error/500.html"), 500
