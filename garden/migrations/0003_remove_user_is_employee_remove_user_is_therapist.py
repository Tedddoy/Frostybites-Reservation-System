# Generated by Django 5.0.4 on 2024-10-30 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0002_user_is_therapist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_employee',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_therapist',
        ),
    ]
