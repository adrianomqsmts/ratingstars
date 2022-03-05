from flask import url_for
from app import index, load_user, base
import pytest
from flask_login import login_user, logout_user


def test_app_is_created(app):
    """teste a a aplicação foi criada, com o nome esperado.

    Args:
        app: A Aplicação Flask, como injeção de parâmetro da fixture
    """
    assert app.name == "project.configs.server"


def test_index_status_code_is_200(client, db):
    """Testa o status code da página inicial da aplicação."""
    response = client.get(url_for("index"))
    assert response.status_code == 200


@pytest.mark.usefixtures("test_with_authenticated_user")
def test_index_redirect_dashboard_status_code_is_200_and_path_is_dashboard(client, db):
    """Testa o status code da página inicial da aplicação, onde deve ser redirecionado para a página de dashboard.

    @test_with_authenticated_user
        Testar o caso em que o usuário está autenticado.

    Args:
        user: O usuário a ser autenticado.
    """
    with client:
        response = client.get(url_for("index"), follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == url_for("ratebp.dashboard")
        logout_user()


def test_load_user(simple_user, db):
    loaded_user = load_user(simple_user.id)
    assert simple_user == loaded_user, "usuário ausente no banco de dados"


def test_config_is_loaded(config):
    """Verificando as configurações do projeto.

    Args:
        config: Configurações geradas pela biblioteca pytest-flask
    """
    assert config["DEBUG"] == True
    assert config["CKEDITOR_PKG_TYPE"] == "basic"
