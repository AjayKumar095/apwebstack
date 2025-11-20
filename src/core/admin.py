from django.contrib import admin
from .models import Icon, SectionType

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    search_fields = ("name", "class_name")
    list_display = ("name", "class_name")
    
@admin.register(SectionType)
class SectionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "use_heading", "use_paragraph", "use_image", "use_bullets", "use_rows")
    search_fields = ("name",)