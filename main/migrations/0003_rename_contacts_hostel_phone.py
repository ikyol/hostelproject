# Generated by Django 3.2.6 on 2021-08-18 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_hostel_contacts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostel',
            old_name='contacts',
            new_name='phone',
        ),
    ]