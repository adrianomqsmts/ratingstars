from flask import Flask, render_template
from flask_ckeditor import CKEditor

#Login
from flask_login import LoginManager, current_user

# Database
from database import db
from flask_migrate import Migrate

# VIEWS
from views.view_user import userbp
from views.view_rate import ratebp

# MODELS
from models.model_user import UsersModel

# Configs
app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)
db.app = app
migrate = Migrate(app, db)
ckeditor = CKEditor()

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.login'

@login_manager.user_loader
def load_user(user_id):
  return UsersModel.query.get(int(user_id))


# BluePrints
app.register_blueprint(userbp, url_prefix="/user")
app.register_blueprint(ratebp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    ckeditor.init_app(app)
        
    db.create_all(app=app)

    app.run(host="127.0.0.1", port=8000, debug=True)
