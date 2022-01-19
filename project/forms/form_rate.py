from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    SubmitField,
    IntegerRangeField,
    IntegerField,
    ValidationError,
    RadioField,
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class RateForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    original_title = StringField("Original Title")
    # content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Content", validators=[DataRequired()])
    rate = RadioField(
        "Rate",
        validators=[DataRequired()],
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
    )
    submit = SubmitField("Rate")
