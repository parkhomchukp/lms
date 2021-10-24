"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from student.views import (
    hello,
    get_students,
    create_student,
    update_student,
    delete_student,
    create_teacher,
    sort_students_by_course,
    get_teachers,
    delete_teacher,
    update_teacher,
    sort_teachers_by_course,
)

app_name = 'students'

urlpatterns = [
    path("", get_students, name="list"),
    path("teachers/", get_teachers, name="teachers-list"),
    path("new/", create_student, name="create"),
    path("edit/<int:pk>/", update_student, name="update"),
    path("delete/<int:pk>/", delete_student, name="delete"),
    path("delete-teacher/<int:pk>/", delete_teacher, name="delete-teacher"),
    path("create-teacher/", create_teacher, name="create-teacher"),
    path("edit-teacher/<int:pk>/", update_teacher, name="update-teacher"),
    path(
        "teachers-by-course/<str:course_name>",
        sort_teachers_by_course,
        name="teachers-by-course",
    ),
    path(
        "students-by-course/<str:course_name>",
        sort_students_by_course,
        name="by-course",
    ),
]

handler404 = "student.views.error_404"
