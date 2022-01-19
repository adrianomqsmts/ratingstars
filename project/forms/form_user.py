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
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    about = CKEditorField("Content", validators=[DataRequired()])
    #profile_pic = FileField("Profile Pic")
    submit = SubmitField("Update")


class UpdatePicForm(FlaskForm):
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Update")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords need to be equal"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Register")
