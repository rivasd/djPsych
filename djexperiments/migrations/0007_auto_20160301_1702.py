# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-01 22:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djexperiments', '0006_auto_20160301_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='research_group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
