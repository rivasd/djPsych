# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-28 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djexperiments', '0009_auto_20160728_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='PayPal_Live_ID',
            field=models.CharField(blank=True, help_text='The PayPAl Live AppID for your experiment', max_length=64, null=True),
        ),
    ]
