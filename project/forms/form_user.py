from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    SubmitField,
    EmailField,
    PasswordField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    #content = CKEditorField("Content", validators=[DataRequired()])
    # author = StringField('Author', validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    password_hash = PasswordField("Password", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    color = StringField("Color")
    password_hash = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Passwords need to be equal"),
        ],
    )
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
