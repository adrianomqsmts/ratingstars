from database import db
from datetime import datetime, date


class RatingModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  original_title = db.Column(db.String(255))
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text, nullable=False)
  rate = db.Column(db.Integer, nullable=False)
  date_posted = db.Column(db.DateTime, default=datetime.utcnow)
  # Foreign Key
  rater_id = db.Column(db.Integer, db.ForeignKey('users_model.id'))
  