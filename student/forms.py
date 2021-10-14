from django.core.validators import ValidationError
from django.forms import ModelForm, TextInput

from student.models import Student


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthdate', 'enroll_date', 'graduate_date']

        widgets = {'phone_number': TextInput(attrs={'pattern': '\d{10,14}'})}

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        return self.normalize_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        return self.normalize_name(last_name)

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        if first_name == last_name:
            raise ValidationError('First and last names can\'t be equal')

        enroll_date = cleaned_data['enroll_date']
        graduate_date = cleaned_data['graduate_date']
        if enroll_date >= graduate_date:
            raise ValidationError('Enroll date must be less then graduate date')

        return cleaned_data