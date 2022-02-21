from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    SubmitField,
    IntegerRangeField,
    IntegerField,
    ValidationError,
    RadioField,
    SelectField,
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from project.models.model_rate import TypeRate


class SearchForm(FlaskForm):
  search = StringField('Search', validators=[DataRequired()])
  submit = SubmitField('Search')


class RateForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    original_title = StringField("Original Title")
    # content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Content", validators=[DataRequired()])
    rate_type = SelectField("Type", choices=[e.value for e in TypeRate])
    rate_pic = FileField("Rate Pic")
    rate = RadioField(
        "Rate",
        validators=[DataRequired()],
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
    )
    submit = SubmitField("Rate")
