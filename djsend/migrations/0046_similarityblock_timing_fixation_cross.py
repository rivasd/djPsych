# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-02 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0045_auto_20170201_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='similarityblock',
            name='timing_fixation_cross',
            field=models.IntegerField(default=1500, help_text='How long to show the fixation cross for in milliseconds.'),
        ),
    ]
