from django.contrib import admin
from .models import Add_Service

# Register your models here.
@admin.register(Add_Service)
class AddServiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['icon']
