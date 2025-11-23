from django.urls import path
from . import views

urlpatterns = [
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
]
