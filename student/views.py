from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage
from django.db.models import Q
from django.forms.utils import ErrorList
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from student.forms import TeacherBaseForm, TeacherUpdateForm, RegistrationStudentForm
from student.models import Student, Course, Teacher
from webargs.djangoparser import use_args
from webargs import fields
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = reverse_lazy("students:login")
    extra_context = {"site_name": "Pavlo"}


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


class CreateStudent(CreateView):
    template_name = "students_create.html"
    model = Student
    fields = "__all__"
    initial = {
        "first_name": "default",
        "last_name": "default",
    }
    success_url = reverse_lazy("students:list")

    def form_valid(self, form):
        form.save(commit=False)
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["dsadas"])
            form._errors["last_name"] = ErrorList(
                [u"You already have an email with that name man."]
            )
            return super().form_invalid(form)
        return super().form_valid(form)


class UpdateStudent(UpdateView):
    model = Student
    template_name = "students_update.html"
    fields = "__all__"
    success_url = reverse_lazy("students:list")


class UserLogin(LoginView):
    pass


class UserLogout(LogoutView):
    template_name = "registration/logged_out.html"


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))


@csrf_exempt
def create_teacher(request):
    form = None
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
    form = None
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


class RegistrationStudent(CreateView):
    template_name = "registration/registration.html"
    form_class = RegistrationStudentForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        return super().form_valid(form)


def error_404(request, exception):
    data = {}
    return render(request, "student/404.html", data)


def send_email(request):
    email = EmailMessage(
        subject="registration lms", body="test text", to=["pavelparkhomchuk@gmail.com"]
    )
    email.send()
    return HttpResponse("Done")
