from django.shortcuts import render
from django.http import HttpResponse
from teachers.models import Teacher
from student.utils import format_records
from webargs.djangoparser import use_args
from webargs import fields


# Create your views here.
@use_args(
    {
        "id": fields.Int(
            required=False
        ),
        "first_name": fields.Str(
            required=False
        ),
        "last_name": fields.Str(
            required=False
        ),
        "email": fields.Str(
            required=False
        ),
        "birthdate": fields.Date(
            required=False
        ),
        "department": fields.Str(
            required=False
        ),
    },
    location="query",
)
def get_teachers(request, params):
    teachers = Teacher.objects.all()

    for param_name, param_value in params.items():
        teachers = teachers.filter(**{param_name: param_value})

    result = format_records(teachers)

    return HttpResponse(result)
