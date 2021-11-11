from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailField
from student.models import Student, Teacher
from django.contrib.auth.forms import UserCreationForm


class RegistrationStudentForm(UserCreationForm):

    email = EmailField(
        max_length=200, help_text="registration without email is not possible!"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class PersonBaseForm(ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "phone_number", "course"]

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]

        return self.normalize_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]

        return self.normalize_name(last_name)

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data["first_name"]
        last_name = cleaned_data["last_name"]
        if first_name == last_name:
            raise ValidationError("First and last names can't be equal")

        return cleaned_data


class StudentCreateForm(PersonBaseForm):
    class Meta(PersonBaseForm.Meta):
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "course",
            "photo",
            "cv",
        ]


class StudentUpdateForm(PersonBaseForm):
    class Meta(StudentCreateForm.Meta):
        pass


class TeacherBaseForm(PersonBaseForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone_number", "course"]


class TeacherUpdateForm(PersonBaseForm):
    class Meta(TeacherBaseForm.Meta):
        pass
