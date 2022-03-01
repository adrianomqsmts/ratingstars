from project.database import db
from datetime import datetime, date
from enum import Enum, auto
from project.models.model_user import UsersModel
from project.models.model_season import SeasonModel


class TypeRate(Enum):
    ANIME = "Anime"
    MOVIE = "Movie"
    SERIES = "Series"
    CARTOON = "Cartoon"


class RatingModel(db.Model):
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
    seasons = db.relationship("SeasonModel",cascade="all,delete", backref="seasons")