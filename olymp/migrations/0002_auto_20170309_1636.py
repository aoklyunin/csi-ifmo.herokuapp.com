# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-09 13:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Students',
            new_name='Student',
        ),
        migrations.RenameField(
            model_name='university',
            old_name='name',
            new_name='long',
        ),
        migrations.AddField(
            model_name='university',
            name='short',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='olymp',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 3, 9, 16, 36, 48, 392358)),
        ),
    ]
