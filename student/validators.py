import datetime
import os

from django.core.exceptions import ValidationError


def no_elon_validator(email):
    if 'elon' in email.lower():
        raise ValidationError('No more Elons, please!')


def domain_validator(email):
    if email.split('@')[1] == 'xyz.com':
        raise ValidationError('Please, use another domain')


def age_validator(birthdate):
    if datetime.datetime.now().year - birthdate.year < 18:
        raise ValidationError('Student should be adult')


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".pdf", ".doc", ".docx", ".txt"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")
