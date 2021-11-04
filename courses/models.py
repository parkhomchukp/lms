import uuid

from django.db import models
from datetime import datetime


# Create your models here.
class Course(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(null=False, max_length=100)
    start_date = models.DateField(null=True, default=datetime.today)
    count_of_students = models.IntegerField(
        null=True,
    )

    def __str__(self):
        return f"{self.name}"
