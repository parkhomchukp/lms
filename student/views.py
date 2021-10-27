from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from student.forms import StudentCreateForm, TeacherBaseForm, TeacherUpdateForm
from student.models import Student, Course, Teacher
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
    courses = Course.objects.all()

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
        context={"students": students, "courses": courses},
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
        request=request, template_name="students_update.html", context={"form": form}
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


def sort_students_by_course(request, course_name):
    students = Student.objects.all().filter(course__name__contains=course_name)
    courses = Course.objects.all()
    return render(
        request=request,
        template_name="students_table.html",
        context={"students": students, "courses": courses},
    )


def get_teachers(request):
    teachers = Teacher.objects.all().order_by("-id")
    courses = Course.objects.all()
    return render(
        request=request,
        template_name="teachers_table.html",
        context={"teachers": teachers, "courses": courses},
    )


def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    teacher.delete()

    return HttpResponseRedirect(reverse("students:teachers-list"))


@csrf_exempt
def update_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)

    if request.method == "POST":
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:teachers-list"))

    elif request.method == "GET":
        form = TeacherUpdateForm(instance=teacher)

    return render(
        request=request, template_name="teachers_update.html", context={"form": form}
    )


def sort_teachers_by_course(request, course_name):
    teachers = Teacher.objects.all().filter(course__name__contains=course_name)
    courses = Course.objects.all()
    return render(
        request=request,
        template_name="teachers_table.html",
        context={"teachers": teachers, "courses": courses},
    )


def error_404(request, exception):
    data = {}
    return render(request, "student/404.html", data)
