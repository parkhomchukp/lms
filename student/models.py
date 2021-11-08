import datetime

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from faker import Faker

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import PeopleManager
from .validators import no_elon_validator, domain_validator, age_validator


# Create your models here.
class ExtendedUser(User):
    people = PeopleManager()

    class Meta:
        proxy = True
        ordering = ("first_name",)

    def some_action(self):
        print(self.username)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, help_text="Contact phone number")
    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/")

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Person(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(
        max_length=60,
        null=False,
        validators=[
            MinLengthValidator(2),
        ],
    )
    last_name = models.CharField(
        max_length=80,
        null=False,
        validators=[
            MinLengthValidator(2),
        ],
    )
    email = models.EmailField(
        max_length=120,
        null=True,
        validators=[no_elon_validator, domain_validator],
        unique=True,
    )
    phone_number = PhoneNumberField(
        unique=True,
        null=True,
    )


class Student(Person):
    course = models.ForeignKey("courses.Course", null=True, on_delete=models.SET_NULL)
    birthdate = models.DateField(
        null=True, default=datetime.date.today, validators=[age_validator]
    )
    enroll_date = models.DateField(
        null=False,
        default=datetime.date.today,
    )
    graduate_date = models.DateField(
        null=True,
        default=datetime.date.today,
    )

    REQUIRED_FIELDS = [
        "email",
    ]
    USERNAME_FIELD = "email"

    def __str__(self):
        return f'{self.full_name()}, {self.age()}, {self.email} ({self.id})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def age(self):
        return datetime.datetime.now().year - self.birthdate.year

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            st = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_time_between(start_date="-30y", end_date="-18y"),
            )
            st.save()
