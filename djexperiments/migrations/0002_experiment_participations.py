# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-03 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djcollect', '0001_initial'),
        ('djuser', '0001_initial'),
        ('djexperiments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='participations',
            field=models.ManyToManyField(through='djcollect.Participation', to='djuser.Subject'),
        ),
    ]
