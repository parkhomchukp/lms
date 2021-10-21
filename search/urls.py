from django.urls import path
from .views import search_students

from . import views

app_name = "search"
urlpatterns = [
    path("", search_students, name="index"),
]
