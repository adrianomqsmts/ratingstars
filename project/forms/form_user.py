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
        name* (StringField): O nome do usuário
        username* (StringField): O nome de usuário
        about* (CKEditorField): Sobre o Usuário
        submit (SubmitField): Compo de Submissão
    """

    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    about = CKEditorField("About you", validators=[DataRequired()])
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
        name* (StringField): O nome do usuário
        username* (StringField): O nome de usuário
        password* (PasswordField): A senha de Usuário
        password2* (PasswordField): A senha de confirmação de Usuário
        about* (CKEditorField): Sobre o Usuário
        profile_pic (FileField): O imagem de perfil do usuário
        email* (EmailField): O email do usuário
        remember (CKEditorField): Se o usuário deve se lembrado ao entrar novamente
        submit (SubmitField): Compo de Submissão
    """

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
    about = CKEditorField("About you", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Register")
