# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-19 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0005_auto_20160611_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
