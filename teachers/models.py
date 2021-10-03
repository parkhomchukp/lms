import datetime

from django.db import models


# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    subject = models.CharField(max_length=80, null=False)
    email = models.EmailField(max_length=120, null=True)
    birthday = models.DateField(null=True, default=datetime.datetime)
