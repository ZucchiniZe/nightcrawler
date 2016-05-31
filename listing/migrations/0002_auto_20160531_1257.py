# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creator',
            options={'ordering': ['first']},
        ),
        migrations.AddField(
            model_name='creator',
            name='url',
            field=models.URLField(default='http://marvel.com/comics/creators'),
        ),
    ]