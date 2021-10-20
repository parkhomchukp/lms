import random

from django.db import models
from faker import Faker
from datetime import datetime


# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    department = models.CharField(max_length=80, null=False)
    email = models.EmailField(max_length=120, null=True)
    birthdate = models.DateField(null=True, default=datetime.today)

    def __str__(self):
        return f'{self.full_name()}, {self.age()} ({self.id})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def age(self):
        return datetime.datetime.now().year - self.birthdate.year

    @classmethod
    def generate_teachers(cls, count):
        faker = Faker()
        departments = [
            "Accounting & Finance",
            "Art & Design",
            "Architecture",
            "Mechanical, Aeronautical & Manufacturing Engineering",
            "Law",
            "Economics & Econometrics",
            "Medicine",
            "Business & Management Studies",
            "Engineering & Technology",
            "Computer Science & Information Systems",
        ]
        for _ in range(count):
            tc = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                department=random.choice(departments),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y", end_date="-18y"),
            )
            tc.save()
