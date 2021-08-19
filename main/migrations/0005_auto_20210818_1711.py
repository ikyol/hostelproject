# Generated by Django 3.2.6 on 2021-08-18 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20210818_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='main.hostel')),
            ],
        ),
        migrations.DeleteModel(
            name='RateLikeFav',
        ),
    ]
