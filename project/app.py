from flask import Flask, render_template
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
app.config.from_object('config')




# BluePrints
app.register_blueprint(userbp, url_prefix='/user')



@app.route("/")
def index():
    users = UsersModel.all()
    form = UserForm()
    return "Hello World"


if __name__ == "__main__":
    db.init_app(app)
    migrate = Migrate(app, db)
    app.run(host="127.0.0.1", port=8000, debug=True)
