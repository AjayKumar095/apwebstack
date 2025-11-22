from django.urls import path
from . import views

urlpatterns = [
    path('form-submit', views.contact_form, name='contact_form'),
    path('', views.contact, name="contact")
]
