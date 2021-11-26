from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView
from marshmallow import fields
from webargs.djangoparser import use_args
from student.models import Student


class SearchStudents(LoginRequiredMixin, ListView):
    template_name = "search_results.html"
    context_object_name = "students"
    login_url = reverse_lazy("students:login")

    @use_args(
        {"q": fields.Str(required=False), "text": fields.Str(required=False)},
        location="query",
    )
    def get_queryset(self, params):
        students = None

        if params["q"] is not None:
            students = Student.objects.filter(
                Q(first_name__contains=params["q"])
                | Q(last_name__contains=params["q"])
                | Q(email__contains=params["q"])
            )
        return students
