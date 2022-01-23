from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from forms.form_rate import RateForm, SearchForm
from models.model_rate import RatingModel, TypeRate
from upload import image_upload, image_remove_and_upload
from database import db
from sqlalchemy import or_

ratebp = Blueprint(
    "ratebp",
    __name__,
)


@ratebp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    rates = RatingModel.query.filter_by(rater_id=current_user.id)
    total_rate = rates.count()
    page = request.args.get("page", 1, type=int)
    rates_page = rates.paginate(page=page, per_page=10)
    return render_template("rate/dashboard.html", rates_page=rates_page)


@ratebp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = RateForm()
    if form.validate_on_submit():
        try:
            # verify if rate_type exists on Enum class
            type_rate = TypeRate(form.rate_type.data).name
        except:
            type_rate = None
            flash("Wrong Type Selected! :(", category="danger")
        finally:
            rate_pic = image_upload(request.files["rate_pic"])
            new_rate = RatingModel(
                original_title=form.original_title.data,
                title=form.title.data,
                content=form.content.data,
                rate=int(form.rate.data),
                rater_id=current_user.id,
                rate_pic=rate_pic,
                rate_type=type_rate,
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
    rate = RatingModel.query.get_or_404(id)
    form = RateForm(rate_type=rate.rate_type.value)  # preselect that rate_type
    if current_user.id == rate.rater_id:
        if form.validate_on_submit():
            rate.title = form.title.data
            rate.original_title = form.original_title.data
            rate.content = form.content.data
            rate.rate = form.rate.data
            try:
                rate.rate_type = TypeRate(form.rate_type.data).name
                try:
                    db.session.add(rate)
                    db.session.commit()
                    flash("Rate Updated successfully!", category="success")
                    return redirect(url_for("ratebp.dashboard"))
                except:
                    flash("Error with database", category="danger")
                    return redirect(url_for("ratebp.update", id=id))
            except:
                flash("Wrong Type Selected! :(", category="danger")
                return redirect(url_for("ratebp.update", id=id))

        form.rate.default = rate.rate
        form.content.data = rate.content
        return render_template("rate/update_rate.html", form=form, rate=rate)
    else:
        flash("You bot allowed to edit that rate!", category="warning")
        return redirect(url_for("ratebp.dashboard"))


@ratebp.route("/delete/<int:id>", methods=["GET"])
@login_required
def delete(id):
    rate = RatingModel.query.get_or_404(id)
    if current_user.id == rate.rater.id:
        try:
            db.session.delete(rate)
            db.session.commit()
            flash("Rate Was Deletd!")
        except:
            flash("Error to deleting the rate...")
        finally:
            return redirect(url_for("ratebp.dashboard"))
    else:
        flash("You cannot delete this post")
        return redirect(url_for("ratebp.dashboard"))


@ratebp.route("/read/<int:id>", methods=["GET"])
@login_required
def read(id):
    rate = RatingModel.query.get_or_404(id)
    return render_template("rate/read_rate.html", rate=rate)


@ratebp.route("/search", methods=["POST"])
@login_required
def search():
    form = SearchForm()
    rating = RatingModel.query
    if form.validate_on_submit():
        search = form.search.data

        title_query = RatingModel.title.like("%" + search + "%")
        title_original_query = RatingModel.original_title.like("%" + search + "%")
        type_rate_query = RatingModel.rate_type.like("%" + search + "%")

        rating = rating.filter(or_(title_query, title_original_query, type_rate_query))
        rating = rating.order_by(RatingModel.date_posted).all()
        return render_template(
            "rate/search_result.html", form=form, search=search, rating=rating
        )
