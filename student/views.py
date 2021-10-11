from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from student.forms import StudentCreateForm
from student.models import Student
from student.utils import format_records
from webargs.djangoparser import use_args
from webargs import fields
from django.urls import reverse


# Create your views here.
def hello(request):
    return HttpResponse('SUCCESS')


@use_args(
    {
        "first_name": fields.Str(
            required=False
        ),
        "text": fields.Str(
            required=False
        )
    },
    location="query",
)
def get_students(request, params):
    form = """
        <form >
          <label>First name:</label><br>
          <input type="text" name="first_name"><br>

          <label>Text:</label><br>
          <input type="text" name="text" placeholder="Enter text to search"><br><br>

          <input type="submit" value="Search">
        </form>
        """

    students = Student.objects.all().order_by('-id')

    for param_name, param_value in params.items():
        if param_value:
            if param_name == 'text':
                students = students.filter(
                    Q(first_name__contains=param_value) |
                    Q(last_name__contains=param_value) |
                    Q(email__contains=param_value)
                )
            else:
                students = students.filter(**{param_name: param_value})

    result = format_records(students)

    response = form + result

    return HttpResponse(response)


@csrf_exempt
def create_student(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    elif request.method == 'GET':
        form = StudentCreateForm()

    form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

    return HttpResponse(form_html)


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

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """

    return HttpResponse(form_html)
