# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0012_auto_20160414_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='similarityblock',
            name='timeout',
            field=models.IntegerField(default=-1, help_text='time limit for the participant before the trial automatically advances'),
        ),
        migrations.AddField(
            model_name='similarityblock',
            name='timeout_message',
            field=models.CharField(blank=True, help_text='message to display if the participant takes too long to respond', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='similarityblock',
            name='timeout_message_en',
            field=models.CharField(blank=True, help_text='message to display if the participant takes too long to respond', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='similarityblock',
            name='timeout_message_es',
            field=models.CharField(blank=True, help_text='message to display if the participant takes too long to respond', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='similarityblock',
            name='timeout_message_fr',
            field=models.CharField(blank=True, help_text='message to display if the participant takes too long to respond', max_length=128, null=True),
        ),
    ]
