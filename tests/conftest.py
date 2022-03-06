from email.mime import application
from unicodedata import name
from flask_login import login_user, logout_user
import pytest
from project.configs.server import server
from app import model_user, url_for, login_manager
import os
from werkzeug.datastructures import FileStorage


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def app(request):
    app = server.app
    server.configure()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd-teste2.sqlite3'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True 
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture(autouse=True)
def app_context(app):
    """Creates a flask app context"""
    with app.app_context():
        yield app


@pytest.fixture
def request_context(app_context):
    """Creates a flask request context"""
    with app_context.test_request_context():
        yield


@pytest.fixture
def client(app_context):
    return app_context.test_client(use_cookies=True)


@pytest.fixture()
def db(app_context):

    db = server.create_database(app_context)

    # seed the database
    user = model_user.UsersModel(
        id=1,
        username="mylyto",
        about="213132",
        name="mylyto",
        email="mylyto@mail.com",
        password="123456789",
        profile_pic="e6dc9403-9beb-11ec-91f0-9c7befa260ac_goku.jpg",
        admin=True,
    )
    db.session.add(user)
    db.session.commit()

    yield db

    # teardown database
    # https://stackoverflow.com/a/18365654/5819113
    db.session.remove()
    db.drop_all()
    db.get_engine(app_context).dispose()



@pytest.fixture
def simple_user():
    user = model_user.UsersModel(
        id=1,
        username="mylyto",
        about="213132",
        name="mylyto",
        email="mylyto@mail.com",
        password="123456789",
        profile_pic="e6dc9403-9beb-11ec-91f0-9c7befa260ac_goku.jpg",
        admin=True,
    )
    return user


@pytest.fixture
def example_image():
    filename = "project/static/images/1dfbd7ce-9b50-11ec-bfc3-9c7befa260ac_goku.jpg"
    fileobj = open(filename, "rb")
    return FileStorage(stream=fileobj, filename="goku.jpg", content_type="image")


@pytest.fixture(scope="function")
def test_with_authenticated_user(simple_user):
    @login_manager.request_loader
    def load_user_from_request(request):
        return model_user.UsersModel.query.first()
