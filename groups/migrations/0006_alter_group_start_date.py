# Generated by Django 3.2.7 on 2021-10-13 08:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_alter_group_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 10, 13, 8, 30, 15, 990967, tzinfo=utc), null=True),
        ),
    ]
