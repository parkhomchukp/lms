from django.shortcuts import render
from django.http import HttpResponse
from teachers.models import Teacher
from student.utils import format_records
from webargs.djangoparser import use_args
from webargs import fields


# Create your views here.
def get_teachers(request):
    teachers = Teacher.objects.all()
    result = format_records(teachers)

    return HttpResponse(result)
