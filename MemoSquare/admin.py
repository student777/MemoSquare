from django.contrib import admin
from . import models

admin.site.register(models.UserDetail)
admin.site.register(models.Memo)
admin.site.register(models.Page)
admin.site.register(models.Clip)
admin.site.register(models.Report)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.LikeComment)
admin.site.register(models.LikeMemo)