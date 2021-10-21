from django.db.models import Q
from django.shortcuts import render
from student.models import Student


# Create your views here.
def search_students(request):

    question = request.GET.get("q")

    if question is not None:
        students = Student.objects.filter(
            Q(first_name__contains=question)
            | Q(last_name__contains=question)
            | Q(email__contains=question)
        )

    return render(
        request=request,
        template_name="search_results.html",
        context={"students": students},
    )
