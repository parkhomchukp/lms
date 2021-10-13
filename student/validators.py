from django.core.exceptions import ValidationError


def no_elon_validator(email):
    if 'elon' in email.lower():
        raise ValidationError('No more Elons, please!')


def domain_validator(email):
    if email.split('@')[1] == 'xyz.com':
        raise ValidationError('Please, use another domain')
