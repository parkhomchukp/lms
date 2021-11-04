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
    sort_teachers_by_course,
    CreateStudent,
    UpdateStudent,
    UserLogin,
    RegistrationStudent,
    UserLogout,
    send_email,
    GetStudents,
    GetStudentsByCourse,
    DeleteStudent,
    CreateTeacher,
    GetTeachers,
    DeleteTeacher,
    UpdateTeacher,
    GetTeachersByCourse,
)

app_name = 'students'

urlpatterns = [
    path("", GetStudents.as_view(), name="list"),
    path("teachers/", GetTeachers.as_view(), name="teachers-list"),
    path("new/", CreateStudent.as_view(), name="create"),
    path("edit/<int:pk>/", UpdateStudent.as_view(), name="update"),
    path("delete/<int:pk>/", DeleteStudent.as_view(), name="delete"),
    path("delete-teacher/<int:pk>/", DeleteTeacher.as_view(), name="delete-teacher"),
    path("create-teacher/", CreateTeacher.as_view(), name="create-teacher"),
    path("edit-teacher/<int:pk>/", UpdateTeacher.as_view(), name="update-teacher"),
    path(
        "teachers-by-course/<str:course_name>",
        GetTeachersByCourse.as_view(),
        name="teachers-by-course",
    ),
    path(
        "students-by-course/<str:course_name>",
        GetStudentsByCourse.as_view(),
        name="by-course",
    ),
    path("login/", UserLogin.as_view(), name="login"),
    path("registration/", RegistrationStudent.as_view(), name="registration"),
    path("logout/", UserLogout.as_view(), name="logout"),
    path("send-email/", send_email, name="send_email"),
]

handler404 = "student.views.error_404"
