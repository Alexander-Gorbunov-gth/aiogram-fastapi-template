from pathlib import Path

from sqladmin import Admin
from sqladmin import ModelView

from core.db import engine
from .system import ImportModule

class AdminSite:
    
    def __init__(self) -> None:
        self.admin_views: list = []

    def reg(self, veiw_class: ModelView) -> ModelView:
        self.admin_views.append(veiw_class)
        return veiw_class


admin_site = AdminSite()


async def init_admin(app):
    """
    Добавлени все view с декоратором @reg для админки
    """
    admin = Admin(app, engine)
    apps = Path("apps")
    ImportModule.found_models_in_project(apps, "admin")
    for view in admin_site.admin_views:
        admin.add_view(view)
