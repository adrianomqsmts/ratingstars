from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from flask_login import UserMixin
from database import db

class UsersModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    profile_pic = db.Column(db.String(), nullable=True)
    # User can have many Posts {post.poster.email}
    # posts = db.relationship("Posts", backref="poster")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw, "sha256")

    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def __repr__(self):
        return f"<Name: {self.name}>"
