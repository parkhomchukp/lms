from django.db import models
from student.models import Person


# Create your models here.
class Teacher(Person):
    course = models.ManyToManyField(to="courses.Course")

    def __str__(self):
        return f"{self.email} ({self.id})"
