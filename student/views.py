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
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = reverse_lazy("students:login")
    extra_context = {"site_name": "Pavlo"}


class GetStudents(ListView):
    template_name = "students_table.html"
    context_object_name = "context"

    @use_args(
        {"first_name": fields.Str(required=False), "text": fields.Str(required=False)},
        location="query",
    )
    def get_queryset(self, params):
        students = Student.objects.all().order_by("-id")
        courses = Course.objects.all()
        for param_name, param_value in params.items():
            if param_value:
                if param_name == "text":
                    students = students.filter(
                        Q(first_name__icontains=param_value)
                        | Q(last_name__icontains=param_value)
                        | Q(email__icontains=param_value)
                    )
                else:
                    students = students.filter(**{param_name: param_value})
        context = {
            "students": students,
            "courses": courses,
        }
        return context


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


class DeleteStudent(DeleteView):
    model = Student
    success_url = reverse_lazy("students:list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CreateTeacher(CreateView):
    template_name = "teacher_create.html"
    model = Teacher
    fields = "__all__"
    initial = {
        "first_name": "default",
        "last_name": "default",
    }
    success_url = reverse_lazy("students:teachers-list")

    def form_valid(self, form):
        form.save(commit=False)
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(
                ["Firs and last names can't be equal"]
            )
            form._errors["last_name"] = ErrorList(
                [u"Teacher with this email already exists"]
            )
            return super().form_invalid(form)
        return super().form_valid(form)


class GetStudentsByCourse(ListView):
    template_name = "students_table.html"
    context_object_name = "context"

    def get_queryset(self):
        course_name = self.kwargs["course_name"]
        students = Student.objects.all().filter(course__name__contains=course_name)
        courses = Course.objects.all()
        context = {"students": students, "courses": courses}
        return context


class GetTeachers(ListView):
    template_name = "teachers_table.html"
    context_object_name = "context"

    def get_queryset(self):
        teachers = Teacher.objects.all().order_by("-id")
        courses = Course.objects.all()
        context = {"teachers": teachers, "courses": courses}
        return context


class DeleteTeacher(DeleteView):
    model = Teacher
    success_url = reverse_lazy("students:teachers-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UpdateTeacher(UpdateView):
    model = Teacher
    fields = "__all__"
    template_name = "teachers_update.html"
    success_url = reverse_lazy("students:teachers-list")


class GetTeachersByCourse(ListView):
    template_name = "teachers_table.html"
    context_object_name = "context"

    def get_queryset(self):
        course_name = self.kwargs["course_name"]
        teachers = Teacher.objects.all().filter(course__name__contains=course_name)
        courses = Course.objects.all()
        context = {"teachers": teachers, "courses": courses}
        return context


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
