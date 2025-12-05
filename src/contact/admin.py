from django.contrib import admin
from .models import Contact_Form, Contact_Meta

# Register your models here.
@admin.register(Contact_Form)
class Contact_FormAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "email")
    list_display =  ("first_name", "email", "message", "date_time")
    
@admin.register(Contact_Meta)
class Contact_MetaAdmin(admin.ModelAdmin):
    list_display = ("meta_title", "meta_description", "meta_keywords")    