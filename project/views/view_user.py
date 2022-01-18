from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from models.model_user import UsersModel
from forms.form_user import UserForm, LoginForm


db = SQLAlchemy()

userbp = Blueprint(
    "userbp",
    __name__,
)


@userbp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                remember = True if form.remember.data else False
                login_user(user, remember=remember)
                return redirect(url_for("ratebp.dashboard"))
            else:
                flash("Wrong Username or Password - Try Again!", category="warning")
        else:
            flash("That User do not exists - Try Again!", category="warning")
    return render_template("user/login.html", form=form)


@userbp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logout!", category="success")
    return redirect(url_for("userbp.login"))


@userbp.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():  # Verify form fields
        user = UsersModel().query.filter_by(email=form.email.data).first()
        if user is None:  # if already exister that user.email
            new_user = UsersModel(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            # Save in Database
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User added Successfully", category="success")
                return redirect(url_for("userbp.login"))
            except:
                flash("error with Database :)", category="danger")
                return redirect(url_for("userbp.register"))
        else:
            flash("User Already Exists", category="info")
        # Clear the form
        form.name.data = ""
        form.email.data = ""
        form.username.data = ""
        form.password.data = ""

    return render_template("user/register.html", form=form)
