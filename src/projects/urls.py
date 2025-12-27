from django.urls import path
from . import views


urlpatterns = [
    path("template-test/", views.project_view, name="template_test"),
    path("template-test/page/<int:id>/", views.project_pagination, name="template_test_detail"),
]
