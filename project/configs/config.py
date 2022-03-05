"""Arquivo de configuração."""

import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.environ["SECRET_KEY"]  # Grabs the folder where the script runs.

SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]

SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]

CKEDITOR_PKG_TYPE = os.environ["CKEDITOR_PKG_TYPE"]

UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]

FLASK_ADMIN_SWATCH = os.environ["FLASK_ADMIN_SWATCH"]

DEBUG = os.environ["DEBUG"]
