from django.contrib import admin
from .models import Icon, Media, ProjectDemo

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    search_fields = ("name", "class_name")
    list_display = ("name", "class_name")
    
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    search_fields = ("file_name",)
    list_display = ("file_name", "date_uploaded")
    
@admin.register(ProjectDemo)
class ProjectDemoAdin(admin.ModelAdmin):
    search_fields = ("title", "category")  
    list_display = ("title", "category", "uploaded_at", "is_active")