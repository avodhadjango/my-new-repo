# Generated by Django 4.2.16 on 2024-11-05 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tourist_apps', '0004_cart_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='New',
            new_name='bookings',
        ),
    ]
