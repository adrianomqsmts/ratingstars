"""Módulo com os modelos da Avaliação."""

from datetime import date, datetime
from enum import Enum, auto

from project.configs.server import server

db = server.db


class TypeRate(Enum):
    """Enum com os tipos de Avaliações possíveis."""

    ANIME = "Anime"
    MOVIE = "Movie"
    SERIES = "Series"
    CARTOON = "Cartoon"


class RatingModel(db.Model):
    """Modelo de Avaliação.

    atributos:
        id* (Integer): Identificador da avaliação
        title* (String): O título da avaliação
        original_title (String): O título original da avaliação
        content* (Text): Descrição da Avaliação
        rate_type* (Enum): O tipo da Avaliação
        rate_pic (String): o caminho da imagem da Avaliação
        rate* (Integer): A nota para a Avaliação
        date_posted (Datetime): A data em que a avaliação foi criada
        rater_id (Integer): O identificador do usuário que realizou a avaliação
        seasons (SeasonModel): As temporadas relacionadas com a avaliação
    """

    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rate_type = db.Column(db.Enum(TypeRate), default=TypeRate.MOVIE)
    rate = db.Column(db.Integer, nullable=False)
    rate_pic = db.Column(db.String(), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key
    rater_id = db.Column(db.Integer, db.ForeignKey("users_model.id"))
    # User can have many Rates {post.rater.email}
    seasons = db.relationship("SeasonModel", cascade="all,delete", backref="seasons")
