# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_auto_20161222_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
