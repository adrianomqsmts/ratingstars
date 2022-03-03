"""Módulo com os modelos da temporadas."""

from datetime import date, datetime

from project.configs.server import server

db = server.db


class SeasonModel(db.Model):
    """Modelo da Temporada.

    atributos:
        id* (Integer): Identificador da temporada
        season* (Integer): O número da temporada
        title* (String): O título da temporada
        content* (Text): Descrição da temporada
        season_pic (String): o caminho da imagem da temporada
        rate* (Integer): A nota para a temporada
        date_posted (Datetime): A data em que a temporada foi criada
        rate_id (Integer): O identificador da avaliação relacionada com a temporada
    """

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=True)
    content = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    season_pic = db.Column(db.String(), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key
    rate_id = db.Column(db.Integer, db.ForeignKey("rating_model.id"))
