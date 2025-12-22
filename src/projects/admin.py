from django.contrib import admin
from .models import ProjectDemo

# Register your models here.
@admin.register(ProjectDemo)
class ProjectDemoAdin(admin.ModelAdmin):
    search_fields = ("title", "category")  
    list_display = ("title", "category", "uploaded_at", "is_active")