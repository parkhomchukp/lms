import datetime
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from faker import Faker

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import PeopleManager, CustomUserManager
from .validators import (
    no_elon_validator,
    domain_validator,
    age_validator,
    validate_file_extension,
)
from django.utils.translation import gettext as _


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=now)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    photo = models.ImageField(
        upload_to="photos",
        default="photos/default.png",
    )
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ExtendedUser(get_user_model()):
    people = PeopleManager()

    class Meta:
        proxy = True
        ordering = ("first_name",)

    def some_action(self):
        print(self.username)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    TYPE_CHOICES = [("TC", "Teacher"), ("ST", "Student"), ("MT", "Mentor")]
    type = models.CharField(
        null=False, max_length=2, default="ST", choices=TYPE_CHOICES
    )
    phone = PhoneNumberField(blank=True, help_text="Contact phone number", region="UA")
    birthdate = models.DateField(blank=True, null=True, default=now)
    photo = models.ImageField(upload_to="media/photos/")
    course = models.ForeignKey("courses.Course", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"


@receiver(post_save, sender=get_user_model())
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
    photo = models.ImageField(
        upload_to="photos",
        default="photos/default.png",
    )
    cv = models.FileField(
        upload_to="cv", default="cv/default.txt", validators=[validate_file_extension]
    )
    number_of_referals = models.IntegerField(default=0, null=True)

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


class Invite:
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4(), editable=False
    )
    student = models.ForeignKey("student.Student", null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey("student.Course", null=True, on_delete=models.SET_NULL)
    recipient_first_name = models.CharField(
        null=False, max_length=100, validators=[MinLengthValidator(2)]
    )
    recipient_last_name = models.CharField(
        null=False, max_length=100, validators=[MinLengthValidator(2)]
    )
