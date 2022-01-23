from flask import Flask, render_template
from flask_ckeditor import CKEditor

# Login
from flask_login import LoginManager, current_user

# Database
from database import db
from flask_migrate import Migrate

# VIEWS
from views.view_user import userbp
from views.view_rate import ratebp
from views.view_season import seasonbp

# MODELS
from models.model_user import UsersModel
from models.model_rate import RatingModel
from models.model_season import SeasonModel

# FORMS
from forms.form_rate import SearchForm

# ADMIN
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from admin import *

# Configs
app = Flask(__name__)
app.config.from_object("config")

# Initialize
db.init_app(app)
db.app = app
migrate = Migrate(app, db)
ckeditor = CKEditor()

# ADMIN
admin = Admin(
    app, name="Admin", template_mode="bootstrap4", index_view=AdminModelView()
)
# ADMIN MODELS
admin.add_view(
    UsersModelView(
        UsersModel,
        db.session,
        name="Users",
        menu_icon_type="fa",
        menu_icon_value="fa-list",
    )
)
admin.add_view(
    RateModelView(
        RatingModel,
        db.session,
        name="Rating",
        menu_icon_type="fa",
        menu_icon_value="fa-list",
    )
)
admin.add_view(
    SeasonModelView(
        SeasonModel,
        db.session,
        name="Season",
        menu_icon_type="fa",
        menu_icon_value="fa-list",
    )
)


# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "userbp.login"


@login_manager.user_loader
def load_user(user_id):
    return UsersModel.query.get(int(user_id))


# BluePrints
app.register_blueprint(userbp, url_prefix="/user")
app.register_blueprint(ratebp)
app.register_blueprint(seasonbp, url_prefix="/season")


# Pass Stuff TO navbar
@app.context_processor
def base():
    search = SearchForm()
    return dict(search=search)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for(ratebp.dashboard))
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def error_on_server(e):
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    ckeditor.init_app(app)

    db.create_all(app=app)

    app.run(host="127.0.0.1", port=8000, debug=True)
