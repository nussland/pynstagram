# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 15:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_photo_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='thumbnail',
        ),
    ]