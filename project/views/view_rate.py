from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from forms.form_rate import RateForm
from models.model_rate import RatingModel

from database import db

ratebp = Blueprint(
    "ratebp",
    __name__,
)


@ratebp.route("/dashboard")
@login_required
def dashboard():
    rates = RatingModel.query.filter_by(rater_id=current_user.id).all()
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
            rate=int(form.rate.data),
            rater_id=current_user.id,
        )

        try:
            db.session.add(new_rate)
            db.session.commit()
            flash("Rate added successfully!", category="success")
            return redirect(url_for("ratebp.dashboard"))
        except:
            flash("Error with database", category="danger")
    return render_template("rate/create_rate.html", form=form)


@ratebp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    form = RateForm()
    rate = RatingModel.query.get_or_404(id)
    if current_user.id == rate.rater_id:
        if form.validate_on_submit():
            rate.title = form.title.data
            rate.original_title = form.original_title.data
            rate.content = form.content.data
            rate.rate = form.rate.data
            try:
                db.session.add(rate)
                db.session.commit()
                flash("Rate Updated successfully!", category="success")
                return redirect(url_for("ratebp.dashboard"))
            except:
                flash('Error with database', category="danger")
                return redirect(url_for("ratebp.update",id=id))
        form.original_title.data = rate.original_title
        form.title.data = rate.title
        form.content.data = rate.content
        
        print(form.rate)
        form.rate.default = rate.rate
        return render_template("rate/update_rate.html", form=form, rate=rate)
    else:
        flash("You bot allowed to edit that rate!", category="warning")
        return redirect(url_for("ratebp.dashboard"))


@ratebp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
  rate = RatingModel.query.get_or_404(id)
  if current_user.id == rate.rater.id:
    try:
      db.session.delete(rate)
      db.session.commit()
      flash('Rate Was Deletd!')
    except:
      flash("Error to deleting the rate...")
    finally:
      return redirect(url_for('ratebp.dashboard'))
  else:
    flash("You cannot delete this post")
    return redirect(url_for('ratebp.dashboard'))