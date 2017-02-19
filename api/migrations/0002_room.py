# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('creation_time', models.DateTimeField()),
                ('radius', models.FloatField()),
                ('expire_time', models.DateTimeField()),
                ('image_url', models.CharField(max_length=500)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UserProxy')),
            ],
        ),
    ]