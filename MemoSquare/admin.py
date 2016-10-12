from django.contrib import admin
from . import models

admin.site.register(models.UserDetail)
admin.site.register(models.Memo)
admin.site.register(models.Page)