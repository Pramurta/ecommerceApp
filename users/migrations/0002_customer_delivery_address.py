# Generated by Django 4.2.13 on 2024-05-21 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='delivery_address',
            field=models.CharField(default=None, max_length=2000),
        ),
    ]