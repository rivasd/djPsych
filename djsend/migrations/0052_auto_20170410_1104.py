# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-10 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0051_auto_20170215_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='abxblock',
            name='timing_fixation_cross',
            field=models.IntegerField(default=500, help_text='How long to show the fixation cross for in milliseconds.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveylikertblock',
            name='preamble',
            field=models.CharField(blank=True, help_text='Small text to display above the likert scale', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='surveylikertblock',
            name='preamble_en',
            field=models.CharField(blank=True, help_text='Small text to display above the likert scale', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='surveylikertblock',
            name='preamble_es',
            field=models.CharField(blank=True, help_text='Small text to display above the likert scale', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='surveylikertblock',
            name='preamble_fr',
            field=models.CharField(blank=True, help_text='Small text to display above the likert scale', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='audioabxblock',
            name='timing_feedback',
            field=models.IntegerField(blank=True, default=1000, help_text='How long to show the feedback message for in milliseconds.'),
        ),
    ]
