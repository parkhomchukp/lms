from django.db import models


# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=80, null=False)
    number_of_members = models.IntegerField(null=False)
