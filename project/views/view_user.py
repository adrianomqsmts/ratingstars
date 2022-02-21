from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from project.database import db
from project.models.model_user import UsersModel
from project.forms.form_user import UserForm, LoginForm, UpdateForm, UpdatePicForm
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from project.upload import image_upload, image_remove_and_upload


userbp = Blueprint(
    "userbp",
    __name__,
)


@userbp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(username=form.username.data).first()
        if user: # If username exists
            if user.verify_password(form.password.data): # verify if user use correct pw
                remember = True if form.remember.data else False # verify if remember is select
                login_user(user, remember=remember) # login that user
                return redirect(url_for("ratebp.dashboard"))
            else: 
                flash("Wrong Username or Password - Try Again!", category="warning")
        else:
            flash("That User do not exists - Try Again!", category="warning")
    return render_template("user/login.html", form=form)


@userbp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user() # logout current user
    flash("Logout!", category="success")
    return redirect(url_for("userbp.login"))


@userbp.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():  # Verify form fields
        email = UsersModel().query.filter_by(email=form.email.data).first()
        username = UsersModel().query.filter_by(email=form.email.data).first()
        if (username is None) and (email is None):  # if not exist that user.email and that user.username
            # Upload file and get its name
            profile_pic = image_upload(request.files["profile_pic"])

            new_user = UsersModel(
                name=form.name.data,
                username=form.username.data,
                about=form.about.data,
                email=form.email.data,
                password=form.password.data,
                profile_pic=profile_pic,
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
    user = UsersModel.query.get_or_404(id) # get current user if exists
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
        image_remove_and_upload(request.files["profile_pic"], user.profile_pic)
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
