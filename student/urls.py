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
    CreateStudent,
    UpdateStudent,
    UserLogin,
    RegistrationStudent,
    UserLogout,
    GetStudents,
    GetStudentsByCourse,
    DeleteStudent,
    ActivateUser,
    Error404,
)

app_name = 'students'

urlpatterns = [
    path("", GetStudents.as_view(), name="list"),
    path("new/", CreateStudent.as_view(), name="create"),
    path("edit/<int:pk>/", UpdateStudent.as_view(), name="update"),
    path("delete/<int:pk>/", DeleteStudent.as_view(), name="delete"),
    path(
        "students-by-course/<str:course_name>",
        GetStudentsByCourse.as_view(),
        name="by-course",
    ),
    path("login/", UserLogin.as_view(), name="login"),
    path("registration/", RegistrationStudent.as_view(), name="registration"),
    path("logout/", UserLogout.as_view(), name="logout"),
    path("activate/<str:uuid64>/<str:token>", ActivateUser.as_view(), name="activate"),
]

handler404 = Error404.as_view()
