"""Módulo principal do Server que irá centralizar todas a configuração da aplicação."""

import os

from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class __Server:
    """Servidor da aplicação."""

    def __init__(
        self,
        template_folder: str = "../../project/templates",
        static_folder: str = "../../project/static",
    ) -> None:
        """Class Initialization Function. Gets called when the object is created."""
        self.app = Flask(
            __name__, template_folder=template_folder, static_folder=static_folder
        )
        self.db = SQLAlchemy()
        self.migrate = Migrate(self.app, self.db, render_as_batch=True)
        self.ckeditor = CKEditor()
        self.login_manager = LoginManager()

    def configure(self) -> bool: # pragma: no cover
        """Configura a aplicação, o banco de dados, CKEditor e cria a base de dados.

        Returns:
            bool: Retorna True se as configurações foram realizadas com sucesso, caso contrário, retorna False.
        """
        try:
            self.app.config.from_object("project.configs.config")
            self.db.init_app(app=self.app)
            self.ckeditor.init_app(self.app)
            self.login_manager.init_app(self.app)
            return True
        except:
            return False

    def run(self) -> Flask: # pragma: no cover
        """Executar o Servidor."""
        self.app.run()
        return self.app
    
    def create_database(self) -> SQLAlchemy:  # pragma: no cover
        with self.app.test_request_context():
            self.db.create_all()
        return self.db


server = __Server()
