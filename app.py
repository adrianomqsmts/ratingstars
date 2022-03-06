"""Aplicação centralizadora do FLASK."""

from typing import Any
import os

from flask import Response, redirect, render_template, url_for
from flask_login import LoginManager, current_user
from itsdangerous import json

from project.configs.server import server
from project.forms.form_rate import RateForm, SearchForm
from project.forms.form_season import SeasonForm
from project.forms.form_user import LoginForm, UpdateForm, UpdatePicForm, UserForm
from project.models import model_admin, model_rate, model_season, model_user
from project.views.view_handler import errorsbp
from project.views.view_rate import ratebp
from project.views.view_season import seasonbp
from project.views.view_user import userbp

# Sever Variables
server.configure()
app = server.app
db = server.create_database()

# BluePrints
app.register_blueprint(userbp, url_prefix="/user")
app.register_blueprint(ratebp)
app.register_blueprint(seasonbp, url_prefix="/season")
app.register_blueprint(errorsbp)

# Login
login_manager = server.login_manager
login_manager.login_view = "userbp.login"


@login_manager.user_loader
def load_user(user_id: str) -> Any:
    """Carrega o usuário atual da aplicação.

    Args:
        user_id (str): O identificador do usuário.

    Returns:
        Any: Retorna a consulta ao banco de dado, com o objeto do usuário.
    """
    return model_user.UsersModel.query.get(int(user_id))


# Pass Stuff TO navbar
@app.context_processor
def base() -> dict:
    """Retorna o formulário de pesquisa rápida da barra de menus para o contexto de toda a aplicação.

    Returns:
        dict: Contexto com search_form dado o formulário de pesquisa rápida
    """
    search_form = SearchForm()
    return dict(search_form=search_form)


@app.route("/")
def index() -> Response:
    """Página inicial da Aplicação.

    Returns:
        Union[Response, str]: Index | Dashboard
    """
    if current_user.is_authenticated:
        return redirect(url_for("ratebp.dashboard"))
    return render_template("index.html")


if __name__ == "__main__":  # pragma: no cover
    db = server.create_database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
