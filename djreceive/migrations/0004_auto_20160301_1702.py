# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-01 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djreceive', '0003_run_used_trials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='browser',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='browser_version',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
