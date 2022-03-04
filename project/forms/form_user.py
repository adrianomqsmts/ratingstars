"""Módulo dos formulários relativos aos usuários da aplicação."""

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    """Formulário de Login.

    atributos:
        username* (StringField): O nome de usuário
        password* (PasswordField): A senha de Usuário
        remember (CKEditorField): Se o usuário deve se lembrado ao entrar novamente
        submit (SubmitField): Compo de Submissão
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateForm(FlaskForm):
    """Formulário de atualização de usuário.

    atributos:
        name* (StringField): O nome do usuário, min=3, max=255
        username* (StringField): O nome de usuário, mim=5, max=50
        about* (CKEditorField): Sobre o Usuário
        submit (SubmitField): Compo de Submissão
    """

    name = StringField("Name*", validators=[DataRequired(), Length(min=3, max=255)])
    username = StringField(
        "Username*", validators=[DataRequired(), Length(min=5, max=50)]
    )
    about = CKEditorField("About you*", validators=[DataRequired(), Length(max=500)])
    # profile_pic = FileField("Profile Pic")
    submit = SubmitField("Update")


class UpdatePicForm(FlaskForm):
    """Formulário de atualização da foto de perfil do usuário.

    atributos:
        profile_pic* (FileField): O imagem de perfil do usuário
        submit (SubmitField): Compo de Submissão
    """

    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Update")


class UserForm(FlaskForm):
    """Formulário de criação de usuário.

    atributos:
        username* (StringField): O nome de usuário, min=5, max=255
        password* (PasswordField): A senha de Usuário
        password2* (PasswordField): A senha de confirmação de Usuário
        email* (EmailField): O email do usuário
        submit (SubmitField): Compo de Submissão
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=120)]
    )
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords need to be equal"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")
