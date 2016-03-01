# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-29 23:57
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djcollect', '0002_auto_20160226_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='finished',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='participation',
            name='parameters',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
