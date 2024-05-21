# Generated by Django 4.2.13 on 2024-05-18 07:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('passportNumber', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Password must be 3-30 characters long and can only contain letters, numbers, and underscores.', regex='^[\\w]{3,30}$')])),
            ],
        ),
    ]
