from sqladmin import ModelView

from .models.user import FastApiUser
from core.admin import admin_site


@admin_site.reg
class UserAdmin(ModelView, model=FastApiUser):
    column_list = [FastApiUser.id, FastApiUser.name]
    