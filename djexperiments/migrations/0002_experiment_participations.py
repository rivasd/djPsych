# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djuser', '0001_initial'),
        ('djcollect', '0001_initial'),
        ('djexperiments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='participations',
            field=models.ManyToManyField(through='djcollect.Participation', to='djuser.Subject'),
        ),
    ]
