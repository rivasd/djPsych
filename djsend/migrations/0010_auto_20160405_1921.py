# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-05 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0009_auto_20160323_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='simcatglobalsetting',
            name='length',
            field=models.PositiveIntegerField(default=40, help_text='How many stimuli pairs should be created'),
        ),
        migrations.AddField(
            model_name='simcatglobalsetting',
            name='practices',
            field=models.PositiveIntegerField(default=5, help_text='How many practice trials should be run before starting the real task'),
        ),
    ]
