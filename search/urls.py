from django.urls import path

from .views import SearchStudents

app_name = "search"
urlpatterns = [
    path("", SearchStudents.as_view(), name="index"),
]
