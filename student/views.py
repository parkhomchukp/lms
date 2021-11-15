from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage
from django.db.models import Q
from django.forms.utils import ErrorList
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from student.forms import RegistrationStudentForm
from student.models import Student, ExtendedUser
from courses.models import Course
from webargs.djangoparser import use_args
from webargs import fields
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
    RedirectView,
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from student.services.emails import send_registration_email
from student.token_generator import TokenGenerator


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = reverse_lazy("students:login")
    extra_context = {"site_name": "Pavlo"}


class GetStudents(LoginRequiredMixin, ListView):
    template_name = "students_table.html"
    context_object_name = "context"
    login_url = reverse_lazy("students:login")

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


class CreateStudent(LoginRequiredMixin, CreateView):
    template_name = "students_create.html"
    model = Student
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "course",
    ]
    success_url = reverse_lazy("students:list")
    login_url = reverse_lazy("students:login")

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


class UpdateStudent(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = "students_update.html"
    fields = "__all__"
    success_url = reverse_lazy("students:list")
    login_url = reverse_lazy("students:login")


class UserLogin(LoginView):
    def get_redirect_url(self):
        return reverse_lazy("index")


class UserLogout(LogoutView):
    template_name = "registration/student_logged_out.html"


class DeleteStudent(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("students:list")
    login_url = reverse_lazy("students:login")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegistrationStudent(CreateView):
    template_name = "registration/registration.html"
    form_class = RegistrationStudentForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(request=self.request, user_instance=self.object)
        return super().form_valid(form)


class GetStudentsByCourse(LoginRequiredMixin, ListView):
    template_name = "students_table.html"
    context_object_name = "context"
    login_url = reverse_lazy("students:login")

    def get_queryset(self):
        course_name = self.kwargs["course_name"]
        students = Student.objects.all().filter(course__name__contains=course_name)
        courses = Course.objects.all()
        context = {"students": students, "courses": courses}
        return context


class ActivateUser(RedirectView):
    url = reverse_lazy("teachers:create")

    def get(self, request, uuid64, token, *args, **kwargs):

        try:
            user_pk = force_bytes(urlsafe_base64_decode(uuid64))
            current_user = User.objects.get(pk=user_pk)
        except (User.DoesNotExist, ValueError, TypeError):
            return HttpResponse("Wrong data")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user)
            return super().get(request, *args, **kwargs)
        return HttpResponse("Wrong data")


class Error404(TemplateView):
    template_name = "student/404.html"
