from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from teachers.models import Teacher
from .forms import TeacherCreateForm
from .utils import format_records
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


@csrf_exempt
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))
    elif request.method == 'GET':
        form = TeacherCreateForm()

    form_html = f"""
            <form method="POST">
              {form.as_p()}
              <input type="submit" value="Create">
            </form>
            """

    return HttpResponse(form_html)
