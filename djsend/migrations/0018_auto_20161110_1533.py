# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-10 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0017_auto_20161103_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratingblock',
            name='responses',
        ),
        migrations.AddField(
            model_name='ratingblock',
            name='response',
            field=models.CharField(choices=[('boxes', 'boxes'), ('slider', 'slider')], default='slider', help_text='Choice between displaying a slider or choices in boxes for response', max_length=16),
        ),
    ]
