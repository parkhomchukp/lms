import random
from django.db import models
from faker import Faker
from django.utils.timezone import now


# Create your models here.
class Group(models.Model):
    start_date = models.DateField(null=True, default=now())
    group_name = models.CharField(max_length=80, null=False)
    number_of_members = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.id}, {self.group_name}, {self.number_of_members}'

    @classmethod
    def generate_groups(cls, count):
        faker = Faker()
        departments = [
            'Accounting & Finance', 'Art & Design', 'Architecture',
            'Mechanical, Aeronautical & Manufacturing Engineering',
            'Law', 'Economics & Econometrics', 'Medicine',
            'Business & Management Studies', 'Engineering & Technology',
            'Computer Science & Information Systems'
        ]
        for _ in range(count):
            start_date = faker.date_between(start_date='-30y', end_date='-1y')
            gr = cls(
                start_date=start_date,
                group_name=f"{random.choice(departments)} ({str(start_date)})",
                number_of_members=random.randint(5, 20)
            )
            gr.save()
