# Generated by Django 3.2.8 on 2021-12-11 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='other_emails',
        ),
        migrations.AddField(
            model_name='wallet',
            name='second_email',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_email', to=settings.AUTH_USER_MODEL),
        ),
    ]
