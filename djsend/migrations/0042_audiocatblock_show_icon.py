# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-27 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0041_auto_20170124_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiocatblock',
            name='show_icon',
            field=models.BooleanField(default=False, help_text='Check this box to have a speaker icon presented in the same time as the sound.'),
        ),
    ]
