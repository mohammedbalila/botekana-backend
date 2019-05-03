from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register([models.Category, models.SubCategory, models.Brand])
