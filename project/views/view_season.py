"""View do da avaliação por temporadas de uma dada avaliação única."""

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
from flask_login import current_user, login_required

from project.configs.server import server
from project.forms.form_season import SeasonForm
from project.models.model_rate import RatingModel
from project.models.model_season import SeasonModel
from project.utils.upload import image_remove_and_upload, image_upload

db = server.db

seasonbp = Blueprint(
    "seasonbp",
    __name__,
)


@seasonbp.route("/create/<int:id>", methods=["GET", "POST"])
@login_required
def create(id: int) -> Response:
    """View de controle e criação de uma avaliação de temporada.

    Decorators:
        @Login_required
        methods=["GET", "POST"]

    Args:
        id (int): Identificador da avaliação que será inserida uma nova temporada

    Returns:
        Union[Response, str]: Dashboard | Create | 404
    """
    form = SeasonForm()
    rate = RatingModel.query.get_or_404(id)
    if rate.rater_id == current_user.id:
        if form.validate_on_submit():
            season_pic = image_upload(request.files["season_pic"])
            new_season = SeasonModel(
                season=int(form.season.data),
                title=form.title.data,
                season_pic=season_pic,
                content=form.content.data,
                rate=form.rate.data,
                rate_id=rate.id,
            )
            try:
                db.session.add(new_season)
                db.session.commit()
            except:
                flash("Erro with database", category="danger")
                return redirect(url_for("sessionbp.create"))
            flash("Season Rating Created Successfully", category="success")
            return redirect(url_for("ratebp.read", id=id))
        return render_template("season/create_season.html", form=form)
    else:
        flash(
            "You Cannot Create a new Rate Season on that Rate. database",
            category="warning",
        )
        return redirect(url_for("ratebp.dashboard"))


@seasonbp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id: int) -> Response:
    """View de controle e criação de uma avaliação de temporada.

    Decorators:
        @Login_required
        methods=["GET", "POST"]

    Args:
        id (int): Identificador da temporada que será atualizada.

    Returns:
        Union[Response, str]: Dashboard | Update | 404
    """
    season = SeasonModel.query.get_or_404(id)
    form = SeasonForm(
        rate=season.rate,
        title=season.title,
        season=season.season,
        content=season.content,
    )
    if current_user.id == season.seasons.rater_id:
        if form.validate_on_submit():

            season.rate = form.rate.data
            season.title = form.title.data
            season.season = form.season.data
            season.content = form.content.data

            try:
                db.session.add(season)
                db.session.commit()
            except:
                flash("Error with database", category="danger")
                return redirect(url_for("seasonbp.update", id=id))
            flash("Rate Updated successfully!", category="success")
            return redirect(url_for("ratebp.read", id=season.rate_id))
        form.rate.default = season.rate
        return render_template("season/update_season.html", form=form, season=season)
    else:
        flash("You bot allowed to edit that rate!", category="warning")
        return redirect(url_for("ratebp.dashboard"))


@seasonbp.route("/delete/<int:id>")
@login_required
def delete(id: int) -> Response:
    """View de controle e remoção de uma avaliação de temporada.

    Decorators:
        @Login_required
        methods=["GET", "POST"]

    Args:
        id (int): Identificador da temporada que será removida.

    Returns:
        Response: Dashboard
    """
    season = SeasonModel.query.get_or_404(id)
    if current_user.id == season.seasons.rater_id:
        try:
            db.session.delete(season)
            db.session.commit()
            flash("season Was Deleted!")
        except:
            flash("Error to deleting the season...")
        finally:
            return redirect(url_for("ratebp.read", id=season.rate_id))
    else:
        flash("You cannot delete this post")
        return redirect(url_for("ratebp.read", id=season.rate_id))
