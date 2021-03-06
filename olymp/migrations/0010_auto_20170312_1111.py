# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-12 11:11
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '0009_auto_20170310_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='student',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='olymp.Man'),
        ),
        migrations.AlterField(
            model_name='work',
            name='olymp',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='olymp.Olymp'),
        ),
        migrations.AlterField(
            model_name='work',
            name='problems',
            field=models.ManyToManyField(blank=True, default=None, to='olymp.ProblemInOlympWithMark'),
        ),
        migrations.AlterField(
            model_name='work',
            name='scan',
            field=models.FileField(blank=True, default=None, storage=django.core.files.storage.FileSystemStorage(location=b'/media/photos'), upload_to=b''),
        ),
    ]
