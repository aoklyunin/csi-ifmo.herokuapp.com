# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-10 05:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '0005_auto_20170309_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='ecspertType',
            field=models.ManyToManyField(to='olymp.ProblemType'),
        ),
        migrations.AlterField(
            model_name='olymp',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 3, 10, 5, 33, 8, 975081)),
        ),
    ]