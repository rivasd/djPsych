# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-07 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0024_auto_20161207_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiocatblock',
            name='timeout_feedback_en',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='audiocatblock',
            name='timeout_feedback_es',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='audiocatblock',
            name='timeout_feedback_fr',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64, null=True),
        ),
    ]
