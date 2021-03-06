# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-06 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0021_auto_20161124_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='similarityblock',
            name='is_audio',
            field=models.BooleanField(default=False, help_text='If you use audio stimuli, check this box.'),
        ),
        migrations.AlterField(
            model_name='audiocatblock',
            name='response_ends_trial',
            field=models.BooleanField(default=True, help_text='Does the trial finishes after the response'),
        ),
    ]
