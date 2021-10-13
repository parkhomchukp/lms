import datetime

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
