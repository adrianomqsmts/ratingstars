"""Módulo dos formulários relativos as avaliações da aplicação."""

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import RadioField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from project.models.model_rate import TypeRate


class SearchForm(FlaskForm):
    """Formulário de pesquisa rápida.

    atributos:
        search* (StringField): Campo de pesquisa
        submit (SubmitField): Compo de Submissão
    """

    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")


class RateForm(FlaskForm):
    """Formulário de Avaliação.

    atributos:
        title* (StringField): O título da avaliação
        original_title (StringField): O título original da avaliação
        content* (CKEditorField): Descrição da Avaliação
        rate_type* (SelectField): O tipo da Avaliação
        rate_pic (FileField): Uma imagem descritiva para a Avaliação
        rate* (RadioField): A nota para a Avaliação
        submit (SubmitField): Compo de Submissão
    """

    title = StringField("Title*", validators=[DataRequired(), Length(max=255)])
    # original_title = StringField("Original Title")
    # content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Content", validators=[Length(max=500)])
    rate_type = SelectField("Type*", choices=[e.value for e in TypeRate])
    rate_pic = FileField("Rate Pic")
    rate = RadioField(
        "Rate*",
        validators=[DataRequired()],
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
    )
    submit = SubmitField("Rate")
