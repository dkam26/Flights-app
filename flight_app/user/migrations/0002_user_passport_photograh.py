# Generated by Django 2.1.7 on 2019-03-06 18:17

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='passport_photograh',
            field=models.ImageField(blank=True, max_length=254, null=True, upload_to=django.core.files.storage.FileSystemStorage(location='/passport_photograhs')),
        ),
    ]