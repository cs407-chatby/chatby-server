# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170216_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='image_url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
