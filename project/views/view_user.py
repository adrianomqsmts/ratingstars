from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from database import db
from models.model_user import UsersModel
from forms.form_user import UserForm, LoginForm, UpdateForm, UpdatePicForm
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from upload import image_upload,  image_remove_and_upload


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
            # Upload file and get name
            profile_pic = image_upload(request.files["profile_pic"])

            new_user = UsersModel(
                name=form.name.data,
                username=form.username.data,
                about=form.about.data,
                email=form.email.data,
                password=form.password.data,
                profile_pic=profile_pic,
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
        form.about.data = ""

    return render_template("user/register.html", form=form)


@userbp.route("/update", methods=["GET", "POST"])
@login_required
def update():
    form = UpdateForm()
    id = current_user.id
    user = UsersModel.query.get_or_404(id)
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
        return render_template("user/update.html", form=form, user=user)


@userbp.route("/update/pic", methods=["GET", "POST"])
@login_required
def pic_update():
    form = UpdatePicForm()
    id = current_user.id
    user = UsersModel.query.get_or_404(id)
    path = "static/images"
    if request.method == "POST":
        image_remove_and_upload(request.files['profile_pic'], user.profile_pic)
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
