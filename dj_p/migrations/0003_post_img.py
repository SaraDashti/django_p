# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-12 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_p', '0002_auto_20171112_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]