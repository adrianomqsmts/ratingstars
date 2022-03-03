"""Módulo de modelos da administração."""

from functools import wraps
from types import FunctionType

from flask import flash, redirect, request, url_for
from flask_admin import expose
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required

from project.models.model_rate import RatingModel
from project.models.model_season import SeasonModel
from project.models.model_user import UsersModel


def admin_required(f: FunctionType) -> FunctionType:
    """Função decorada que irá verificar se o usuário tem permissão de usuário.

    Args:
        f (FunctionType): A função a ser decorada

    Returns:
        FunctionType: A função decorada
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            flash("You do not have permission to view that page", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


class AdminModelView(AdminIndexView):
    """View modelo da administração."""

    def is_visible(self):
        """Define a visibilidade da classe na barra de navegação da área da administração."""
        return False

    @expose("/")
    @login_required
    @admin_required
    def index(self):
        """Define a função que irá trabalhar na informação a ser exibida na página inicial."""
        context = {
            "n_user": UsersModel.query.count(),
            "n_rate": RatingModel.query.count(),
            "n_season": SeasonModel.query.count(),
        }
        return self.render("admin/index.html", context=context)


class UsersModelView(ModelView):
    """Modelo que define quais campos devem estar visíveis e quais propriedades são permitidas para os usuários."""

    edit_modal = True
    can_delete = True
    page_size = 50
    can_edit = True
    column_searchable_list = ("name", "username", "email")
    column_list = ("name", "username", "admin")
    column_labels = dict(
        name="Name",
        email="Email",
        username="Username",
        password_hash="Password",
        about="About",
    )
    column_editable_list = ("name", "username", "email", "admin")
    form_columns = ("name", "username", "email", "password_hash", "admin")
    form_edit_rules = ("name", "username", "email", "admin")

    def is_accessible(self):
        """Define para quem o modelo é acessível."""
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        """Define o redirecionamento em caso de acesso negado."""
        return redirect(url_for("userbp.login", next=request.url))

    def on_model_change(self, form, model, is_created):
        """Atualiza o compo de senha quando o modelo sofre alguma alteração."""
        if form.password_hash.data:
            model.password = form.password_hash.data
        else:
            del form.password_hash


class RateModelView(ModelView):
    """Modelo que define quais campos devem estar visíveis e quais propriedades são permitidas para as Avaliações."""

    edit_modal = True
    can_delete = True
    page_size = 50
    can_edit = True
    column_searchable_list = ("title", "rate_type", "content")
    column_list = ("id", "title", "rate_type", "date_posted")
    column_editable_list = ("title", "rate_type")
    form_columns = ("title", "rate_type", "content", "rater")
    form_create_rules = ("title", "rate_type", "content", "rater")
    form_edit_rules = ("title", "rate_type", "content")


class SeasonModelView(ModelView):
    """Modelo que define quais campos devem estar visíveis e quais propriedades são permitidas para as temporadas."""

    edit_modal = True
    can_delete = True
    page_size = 50
    can_edit = True
    column_searchable_list = ("title", "season", "content")
    column_list = ("id", "title", "season", "seasons")
    column_editable_list = ("title", "season", "date_posted")
    form_columns = ("title", "season", "content", "seasons")
    form_create_rules = ("title", "season", "content", "seasons")
    form_edit_rules = ("title", "season", "content")
