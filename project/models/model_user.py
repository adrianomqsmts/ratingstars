"""Módulo com os modelos da temporadas."""

from datetime import date, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from project.configs.server import server
from project.models.model_rate import RatingModel
from project.models.model_season import SeasonModel

db = server.db


class UsersModel(db.Model, UserMixin):
    """Modelo para usuários.

    atributos:
        id* (Integer): Identificador do usuário
        username* (String): o nome de usuário
        name* (String): o nome do usuário
        about* (Text): Descrição do usuário
        profile_pic (String): o caminho da imagem do usuário
        email* (String): O email do usuário
        password_hash (String): Senha criptografada do Usuário
        admin (Boolean): True se o usuário é um administrador, caso contrário, False.
        rates (RatingModel): As avaliações realizadas pelo usuário.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    about = db.Column(db.Text)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    profile_pic = db.Column(db.String(), nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    # User can have many Rates {post.rater.email}
    rates = db.relationship("RatingModel", cascade="all,delete", backref="rater")

    @property
    def password(self) -> AttributeError:
        """Get Password.

        Raises:
            AttributeError: A senha não é legível

        Returns:
            AttributeError: A senha não é legível
        """
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, pw: str) -> None:
        """Método que realiza a conversão da senha para criptografia na atribuição do atributo password."""
        self.password_hash = generate_password_hash(pw, "sha256")

    def verify_password(self, pw: str) -> bool:
        """Verifica se a senha é igual a senha criptografada.

        Args:
            pw (str): A senha a ser verificada

        Returns:
            bool: Se a senha condiz com a armazenada no Banco de Dados
        """
        return check_password_hash(self.password_hash, pw)

    def __repr__(self) -> str:
        """Altera a representação do objeto usuário, para exibir o seu nome.

        Returns:
            str: <Name: user.username>
        """
        return f"<Name: {self.username}>"
