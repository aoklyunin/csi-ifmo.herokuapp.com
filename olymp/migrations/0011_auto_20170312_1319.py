# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-12 13:19
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations
import olymp.models


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '0010_auto_20170312_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='scan',
            field=olymp.models.CMSFileField(blank=True, default=None, storage=django.core.files.storage.FileSystemStorage(location=b'/media/works'), upload_to=b''),
        ),
    ]
