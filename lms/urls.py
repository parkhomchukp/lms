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
<<<<<<< HEAD
from django.urls import path, include
from student.views import hello, get_students, create_student, update_student
=======
from django.urls import path
from student.views import hello, get_students
from teachers.views import get_teachers
>>>>>>> add729b3819a64d106d0677f9ce8f81b694cde55

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
<<<<<<< HEAD
    path('students/', include('student.urls')),
=======
    path('students/', get_students),
    path('teachers/', get_teachers),
>>>>>>> add729b3819a64d106d0677f9ce8f81b694cde55
]
