"""Módulo dos formulários relativos as temporadas de cada Avaliação."""

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired


class SeasonForm(FlaskForm):
    """Formulário da Temporada.

    atributos:
        season* (IntegerField): O número da Temporada
        title (StringField): O título  da Temporada
        content* (CKEditorField): Descrição da Temporada
        season_pic (FileField): Uma imagem descritiva para a Temporada
        rate* (RadioField): A nota para a Temporada
        submit (SubmitField): Compo de Submissão
    """

    season = IntegerField("Season", validators=[DataRequired()])
    title = StringField("Title")
    season_pic = FileField("Season Pic")
    content = CKEditorField("Content", validators=[DataRequired()])
    rate = RadioField(
        "Rate",
        validators=[DataRequired()],
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
    )
    submit = SubmitField("Rate Season")
