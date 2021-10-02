# Generated by Django 3.2.7 on 2021-10-02 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('subject', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=120, null=True)),
                ('birthday', models.DateField(default=datetime.datetime, null=True)),
            ],
        ),
    ]