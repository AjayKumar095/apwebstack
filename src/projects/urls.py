from django.urls import path
from . import views


urlpatterns = [
    path("templates/", views.project_view, name="template_test"),
    path("templates/page/<int:id>/", views.project_pagination, name="template_test_detail"),
]
