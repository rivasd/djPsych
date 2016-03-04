# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-04 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0003_auto_20160304_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorizationblock',
            name='timing_feedback_duration',
            field=models.IntegerField(help_text='How long to show the feedback for ', null=True),
        ),
        migrations.AlterField(
            model_name='categorizationblock',
            name='timing_post_trial',
            field=models.IntegerField(help_text='Sets the time, in milliseconds, between the current trial and the next trial.', null=True),
        ),
        migrations.AlterField(
            model_name='categorizationblock',
            name='timing_response',
            field=models.IntegerField(help_text='The maximum time allowed for a response. If -1, then the experiment will wait indefinitely for a response.', null=True),
        ),
        migrations.AlterField(
            model_name='categorizationblock',
            name='timing_stim',
            field=models.IntegerField(help_text='How long to show the stimulus for (milliseconds). If -1, then the stimulus is shown until a response is given.', null=True),
        ),
    ]
