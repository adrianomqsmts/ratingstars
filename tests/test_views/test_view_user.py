import pytest
from project.forms.form_user import LoginForm
from project.models.model_user import UsersModel
from flask_login import login_user, logout_user, current_user


from flask import url_for, get_flashed_messages

from project.views.view_user import login


def test_login_page_with_true_user_and_correct_password_is_authenticated(client, db):
    """Tests a view that requires authentication"""
    from flask_login import current_user

    # client is a pytest fixture
    with client as c:
        form = LoginForm()
        form.username.data = 'mylyto'
        form.password.data = '123456789'
        form.remember.data = True
        response = c.post(url_for("userbp.login"), data=form.data)
        assert current_user.is_authenticated == True
 
 
def test_login_page_with_true_user_and_correct_password_status_code_on_dashboard_is_200(client, db):
    """Tests a view that requires authentication"""
    from flask_login import current_user

    # client is a pytest fixture
    with client as c:
        form = LoginForm()
        form.username.data = 'mylyto'
        form.password.data = '123456789'
        form.remember.data = True
        c.post(url_for("userbp.login"), data=form.data)
        response = c.get(url_for("ratebp.dashboard"))
        assert response.status_code == 200
        

def test_login_page_with_true_user_and_incorrect_password_is_not_authenticated(client, db):
    with client as c:
        form = LoginForm()
        form.username.data = 'mylyto'
        form.password.data = 'error'
        form.remember.data = True
        response = c.post(url_for("userbp.login"), data=form.data)
        assert current_user.is_authenticated == False

def test_login_page_with_true_user_and_incorrect_password_flash_message_is_warning(client, db):
    with client as c:
        form = LoginForm()
        form.username.data = 'mylyto'
        form.password.data = 'error'
        form.remember.data = True
        c.post(url_for("userbp.login"), data=form.data)
        flashed_message = get_flashed_messages(with_categories=True)
        assert flashed_message != None, "Não retornou uma mensagem de erro."
        assert 'warning' == flashed_message[0][0], "A mensagem retornada não é uma aviso."
        assert 'Wrong Username or Password - Try Again!' == flashed_message[0][1], "A mensagem está errada"

def test_login_page_with_false_user_flash_message_is_warning(client, db):
    with client as c:
        form = LoginForm()
        form.username.data = 'mylytos'
        form.password.data = '123456789'
        form.remember.data = True
        c.post(url_for("userbp.login"), data=form.data)
        flashed_message = get_flashed_messages(with_categories=True)
        assert flashed_message != None, "Não retornou uma mensagem de erro."
        assert 'warning' == flashed_message[0][0], "A mensagem retornada não é uma aviso."
        assert 'That User do not exists - Try Again!' == flashed_message[0][1], "A mensagem está errada"

def test_login_page_code_status_is_200(client, db):
    response = client.get(url_for("userbp.login"))
    assert response.status_code == 200
 
   
def test_login_page_with_true_user_and_correct_password_is_authenticated(client, db, simple_user):
    """Tests a view that requires authentication"""
    with client as c:
        login_user(simple_user)
        assert current_user.is_authenticated == True
        c.get(url_for("userbp.logout"))
        assert current_user.is_authenticated == False
        

