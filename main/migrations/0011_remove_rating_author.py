# Generated by Django 3.2.6 on 2021-08-19 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_rating_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='author',
        ),
    ]