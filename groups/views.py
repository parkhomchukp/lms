from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from webargs.djangoparser import use_args
from webargs import fields

from .forms import GroupCreateForm
from .models import Group


# Create your views here.
from .utils import format_records


@use_args(
    {
        'group_name': fields.Str(
            required=False
        )
    },
    location='query'
)
def get_groups(request, group_name):
    groups = Group.objects.all()

    if group_name:
        groups = groups.filter(group_name__contains=group_name['group_name'])

    result = format_records(groups)

    return HttpResponse(result)


@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('groups:list'))
    elif request.method == 'GET':
        form = GroupCreateForm()

    form_html = f"""
            <form method="POST">
              {form.as_p()}
              <input type="submit" value="Create">
            </form>
            """

    return HttpResponse(form_html)
