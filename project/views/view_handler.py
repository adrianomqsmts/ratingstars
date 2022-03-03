"""View de controle de requisições de error da aplicação como 404 e 500."""
from project.configs.server import server
from flask import (
    Blueprint,
    Response,
    render_template,
)

handlerbp = Blueprint(
    "handler",
    __name__,
)

@handlerbp.errorhandler(404)
def page_not_found(e)->Response:
    """Page not found.

    Args:
        e (_type_): _description_

    Returns:
        Response: template, 404
    """
    return render_template("error/404.html"), 404


@handlerbp.errorhandler(500)
def error_on_server(e)->Response:
    """Error on server.

    Args:
        e (_type_): _description_

    Returns:
        Response: template, 500
    """
    return render_template("error/500.html"), 500