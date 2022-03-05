"""View dos controle de cadastro e login de Usuários."""

import os
import uuid as uuid
from typing import Union

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.utils import secure_filename

from project.configs.server import server
from project.forms.form_user import LoginForm, UpdateForm, UpdatePicForm, UserForm
from project.models.model_user import UsersModel
from project.utils.upload import image_remove_and_upload, image_upload

db = server.db

userbp = Blueprint(
    "userbp",
    __name__,
)


@userbp.route("/login", methods=["GET", "POST"])
def login() -> Response:
    """View de controle de login do usuário.

    Decorators:
        methods=["GET", "POST"]

    Returns:
        Union[Response, str]: Dashboard | Index
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(username=form.username.data).first()
        if user:  # If username exists
            if user.verify_password(
                form.password.data
            ):  # verify if user use correct pw
                remember = (
                    True if form.remember.data else False
                )  # verify if remember is select
                login_user(user, remember=remember)  # login that user
                return redirect(url_for("ratebp.dashboard"))
            else:
                logout_user()
                flash("Wrong Username or Password - Try Again!", category="warning")
        else:
            logout_user()
            flash("That User do not exists - Try Again!", category="warning")
    return render_template("user/login.html", form=form)


@userbp.route("/logout", methods=["GET", "POST"])
def logout() -> Response:
    """View de controle de logout do usuário.

    Decorators:
        methods=["GET", "POST"]

    Returns:
        Response: Login
    """
    logout_user()  # logout current user
    flash("Logout!", category="success")
    return redirect(url_for("userbp.login"))


@userbp.route("/register", methods=["GET", "POST"])
def register() -> Response:
    """View de controle de cadastro de um novo usuário.

    Decorators:
        methods=["GET", "POST"]

    Returns:
        Union[Response, str]: Login | Register
    """
    form = UserForm()
    if form.validate_on_submit():  # Verify form fields
        email = UsersModel().query.filter_by(email=form.email.data).first()
        username = UsersModel().query.filter_by(email=form.email.data).first()
        if (username is None) and (email is None):
            new_user = UsersModel(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )

            try:  # Save in Database
                db.session.add(new_user)
                db.session.commit()
                flash("User added Successfully", category="success")
                return redirect(url_for("userbp.login"))
            except:
                flash("error with Database :)", category="danger")
                return redirect(url_for("userbp.register"))
        else:
            flash("Username or email Already Exists", category="info")
        # Clear the form
        form.password.data = ""

    return render_template("user/register.html", form=form)


@userbp.route("/update", methods=["GET", "POST"])
@login_required
def update() -> Response:
    """Vire de controle de atualização do usuário atual da aplicação.

    Decorators:
        @Login_required
        methods=["GET", "POST"]

    Returns:
        Union[Response, str]: Dashboard | Update
    """
    id = current_user.id
    user = UsersModel.query.get_or_404(id)  # get current user if exists
    form = UpdateForm(obj=user)
    if form.validate_on_submit():
        user.name = request.form["name"]
        user.username = request.form["username"]
        user.about = request.form["about"]
        try:
            db.session.add(user)
            db.session.commit()
            flash("User Updated Successfully", category="success")
            return redirect(url_for("ratebp.dashboard"))
        except:
            flash("Error with database", category="danger")
            return redirect(url_for("userbp.update"))
    else:
        user.name = user.name if user.name else ""
        return render_template("user/update.html", form=form, user=user)


@userbp.route("/update/pic", methods=["GET", "POST"])
@login_required
def pic_update() -> Response:
    """View de controle de atualização da foto de perfil do usuário atual.

    Decorators:
        @Login_required
        methods=["GET", "POST"]

    Returns:
        Union[Response, str]: Dashboard | UpdatePic
    """
    form = UpdatePicForm()
    id = current_user.id
    user = UsersModel.query.get_or_404(id)
    if request.method == "POST":
        new_profile_pic = image_remove_and_upload(
            request.files["profile_pic"], user.profile_pic
        )
        user.profile_pic = new_profile_pic
        try:
            db.session.add(user)
            db.session.commit()
            flash("Picture Updated Successfully", category="success")
            return redirect(url_for("ratebp.dashboard"))
        except:
            flash("Error with database", category="danger")
            return redirect(url_for("userbp.pic_update"))
    else:
        return render_template("user/pic_update.html", form=form, user=user)
