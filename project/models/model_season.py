from database import db
from datetime import datetime, date


class SeasonModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=True)
    content = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    season_pic = db.Column(db.String(), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Key
    rate_id = db.Column(db.Integer, db.ForeignKey("rating_model.id"))