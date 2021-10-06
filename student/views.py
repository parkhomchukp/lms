from django.shortcuts import render
from django.http import HttpResponse
from student.models import Student
from student.utils import format_records
from webargs.djangoparser import use_args
from webargs import fields


# Create your views here.
def hello(request):
    return HttpResponse('SUCCESS')


@use_args(
    {
        "first_name": fields.Str(
            required=False
        ),
        "last_name": fields.Str(
            required=False
        )
    },
    location="query",
)
def get_students(request, params):
    students = Student.objects.all()

    for param_name, param_value in params.items():
        students = students.filter(**{param_name: param_value})

    result = format_records(students)

    return HttpResponse(result)
