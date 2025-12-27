from django.urls import path
from . import views


urlpatterns = [
    path("", views.project_view, name="template_test"),
    path("demo/page/<int:id>/", views.project_pagination, name="template_test_detail"),
]
