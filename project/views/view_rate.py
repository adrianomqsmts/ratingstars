from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

from forms.form_rate import RateForm
from models.model_rate import RatingModel

db = SQLAlchemy()

ratebp = Blueprint(
    "ratebp",
    __name__,
)


@ratebp.route("/dashboard")
@login_required
def dashboard():
    rates = RatingModel.query.all()
    return render_template("rate/dashboard.html", rates=rates)


@ratebp.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    form = RateForm()
    if form.validate_on_submit():
        new_rate = RatingModel(
            original_title=form.original_title.data,
            title=form.title.data,
            content=form.content.data,
            rate=form.rate.data,
            rater_id=current_user.id,
        )

        try:
            db.session.add(new_rate)
            db.session.commit()
            flash("Rate added successfully!", category="success")
            return redirect(url_for("ratebp.dashboard"))
        except:
            flash("Error with database", category="danger")
    return render_template("rate/rate.html", form=form)
