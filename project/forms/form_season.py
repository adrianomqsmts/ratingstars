from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    RadioField,
    FileField
    )
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class SeasonForm(FlaskForm):
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
