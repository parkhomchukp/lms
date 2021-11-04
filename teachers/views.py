from django.forms.utils import ErrorList
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from teachers.models import Teacher
from courses.models import Course


# Create your views here.
class GetTeachers(ListView):
    template_name = "teachers_table.html"
    context_object_name = "context"

    def get_queryset(self):
        teachers = Teacher.objects.all().order_by("-id")
        courses = Course.objects.all()
        context = {"teachers": teachers, "courses": courses}
        return context


class GetTeachersByCourse(ListView):
    template_name = "teachers_table.html"
    context_object_name = "context"

    def get_queryset(self):
        course_name = self.kwargs["course_name"]
        teachers = Teacher.objects.all().filter(course__name__contains=course_name)
        courses = Course.objects.all()
        context = {"teachers": teachers, "courses": courses}
        return context


class CreateTeacher(CreateView):
    template_name = "teacher_create.html"
    model = Teacher
    fields = "__all__"
    initial = {
        "first_name": "default",
        "last_name": "default",
    }
    success_url = reverse_lazy("teachers:list")

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


class UpdateTeacher(UpdateView):
    model = Teacher
    fields = "__all__"
    template_name = "teachers_update.html"
    success_url = reverse_lazy("teachers:list")


class DeleteTeacher(DeleteView):
    model = Teacher
    success_url = reverse_lazy("teachers:list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
