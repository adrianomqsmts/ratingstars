from flask import Flask, render_template

#Login
from flask_login import LoginManager, current_user

# Database
from database import db
from flask_migrate import Migrate

# VIEWS
from views.view_user import userbp

# MODELS
from models.model_user import UsersModel

# FORMS
from forms.form_user import UserForm


# Configs
app = Flask(__name__)
app.config.from_object("config")

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.login'

@login_manager.user_loader
def load_user(user_id):
  return UsersModel.query.get(int(user_id))


# BluePrints
app.register_blueprint(userbp, url_prefix="/user")


@app.route("/")
def index():
    users = UsersModel.query.all()
    form = UserForm()
    return render_template("index.html")


if __name__ == "__main__":
    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)

    db.create_all(app=app)

    app.run(host="127.0.0.1", port=8000, debug=True)
