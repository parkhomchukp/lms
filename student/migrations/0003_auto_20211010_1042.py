# Generated by Django 3.2.7 on 2021-10-10 07:42

from django.db import migrations, models
import student.validators


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20211010_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=120, null=True, validators=[student.validators.no_elon_validator]),
        ),
    ]