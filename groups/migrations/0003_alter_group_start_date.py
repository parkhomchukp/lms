# Generated by Django 3.2.7 on 2021-10-07 13:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 10, 7, 13, 52, 48, 37338, tzinfo=utc), null=True),
        ),
    ]
