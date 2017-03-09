# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-09 14:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '0004_auto_20170309_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='probleminbank',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='olymp',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 3, 9, 17, 38, 10, 321663)),
        ),
        migrations.AlterField(
            model_name='probleminbank',
            name='text',
            field=models.CharField(default='', max_length=20000),
        ),
    ]