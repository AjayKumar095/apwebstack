from django.contrib import admin
from .models import Icon

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    search_fields = ("name", "class_name")
