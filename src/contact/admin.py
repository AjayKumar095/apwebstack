from django.contrib import admin
from .models import ContactForm, ContactMeta

# Register your models here.
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "email")
    list_display =  ("first_name", "email", "message", "date_time")
    
@admin.register(ContactMeta)
class ContactMetaAdmin(admin.ModelAdmin):
    list_display = ("meta_title", "meta_description", "meta_keywords")    