# Generated by Django 5.0.4 on 2024-05-07 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0014_remove_reservation_customer_reservation_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customers',
        ),
    ]