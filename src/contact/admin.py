from django.contrib import admin
from .models import ContactForm

# Register your models here.
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "email")
    list_display =  ("first_name", "email", "message")