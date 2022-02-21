from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView
from flask_admin import expose
from flask_login import current_user, login_required
from flask import redirect, url_for, request
from project.models.model_user import UsersModel
from project.models.model_rate import RatingModel
from project.models.model_season import SeasonModel
from flask import redirect, url_for, flash
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            flash("You do not have permission to view that page", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


class AdminModelView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    @expose("/")
    @login_required
    @admin_required
    def index(self):
        context = {
            "n_user": UsersModel.query.count(),
            "n_rate": RatingModel.query.count(),
            "n_season": SeasonModel.query.count(),
        }
        return self.render("admin/index.html", context=context)


class UsersModelView(ModelView):
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
    form_edit_rules = ('name', 'username', 'email', "admin")

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("userbp.login", next=request.url))

    def on_model_change(self, form, model, is_created):
        if form.password_hash.data:
            model.password = form.password_hash.data
        else:
            del form.password_hash


class RateModelView(ModelView):
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
