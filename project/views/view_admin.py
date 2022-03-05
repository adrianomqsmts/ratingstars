"""View do Painel de Administração da aplicação."""
from flask_admin import Admin

from project.configs.server import server
from project.models.model_admin import *

app = server.app
db = server.db

admin = Admin(
    app, name="Admin", template_mode="bootstrap4", index_view=AdminModelView()
)

# ADMIN MODELS
admin.add_view(
    UsersModelView(
        UsersModel,
        db.session,
        name="Users",
        menu_icon_type="fa",
        menu_icon_value="fa-list",
    )
)
admin.add_view(
    RateModelView(
        RatingModel,
        db.session,
        name="Rating",
        menu_icon_type="fa",
        menu_icon_value="fa-list",
    )
)
admin.add_view(
    SeasonModelView(
        SeasonModel,
        db.session,
        name="Season",
        menu_icon_type="fa",
        menu_icon_value="fa-list",
    )
)
