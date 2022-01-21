import os

SECRET_KEY = os.urandom(32)  # Grabs the folder where the script runs.

SQLALCHEMY_DATABASE_URI = 'sqlite:///bd.sqlite3'  # Turn off the Flask-SQLAlchemy event system and warning

SQLALCHEMY_TRACK_MODIFICATIONS = False

CKEDITOR_PKG_TYPE = 'basic' # CKEditor theme

UPLOAD_FOLDER = 'static/images'

FLASK_ADMIN_SWATCH = 'cerulean' # Flask-admin theme