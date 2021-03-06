# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-04 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0037_auto_20170104_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlestimblock',
            name='timing_stim',
            field=models.IntegerField(default=-1, help_text='How long to show the stimulus for in milliseconds. If the value is -1, then the stimulus will be shown until the subject makes a response.'),
        ),
    ]
