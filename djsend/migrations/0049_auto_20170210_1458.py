# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-10 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0048_auto_20170210_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='forcedchoiceblock',
            name='timeout_message_en',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when they time out.', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='forcedchoiceblock',
            name='timeout_message_es',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when they time out.', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='forcedchoiceblock',
            name='timeout_message_fr',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when they time out.', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='ratingblock',
            name='timeout_message_en',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when they time out.', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='ratingblock',
            name='timeout_message_es',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when they time out.', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='ratingblock',
            name='timeout_message_fr',
            field=models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when they time out.', max_length=128, null=True),
        ),
    ]
