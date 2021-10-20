from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from student.forms import StudentCreateForm, TeacherBaseForm
from student.models import Student
from student.utils import format_records
from webargs.djangoparser import use_args
from webargs import fields
from django.urls import reverse


# Create your views here.


def hello(request):
    return HttpResponse('SUCCESS')


def index(request):
    return render(request=request, template_name="index.html")


@use_args(
    {"first_name": fields.Str(required=False), "text": fields.Str(required=False)},
    location="query",
)
def get_students(request, params):
    students = Student.objects.all().order_by('-id')

    for param_name, param_value in params.items():
        if param_value:
            if param_name == 'text':
                students = students.filter(
                    Q(first_name__contains=param_value)
                    | Q(last_name__contains=param_value)
                    | Q(email__contains=param_value)
                )
            else:
                students = students.filter(**{param_name: param_value})

    return render(
        request=request,
        template_name="students_table.html",
        context={"students": students},
    )


@csrf_exempt
def create_student(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    elif request.method == 'GET':
        form = StudentCreateForm()

    return render(
        request=request,
        template_name="students_create.html",
        context={"form": form},
    )


@csrf_exempt
def update_student(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == 'POST':
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    elif request.method == 'GET':
        form = StudentCreateForm(instance=student)

    return render(
        request=request, template_name="students_create.html", context={"form": form}
    )


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))


@csrf_exempt
def create_teacher(request):
    if request.method == "POST":
        form = TeacherBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    elif request.method == "GET":
        form = TeacherBaseForm()

    return render(
        request=request,
        template_name="teacher_create.html",
        context={"form": form},
    )


def error_404(request, exception):
    data = {}
    return render(request, "student/404.html", data)
