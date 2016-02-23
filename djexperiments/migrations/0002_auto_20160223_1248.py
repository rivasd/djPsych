# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-23 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djpay', '0002_auto_20160223_1248'),
        ('djcollect', '0001_initial'),
        ('djexperiments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participation',
            name='experiment',
        ),
        migrations.RemoveField(
            model_name='participation',
            name='subject',
        ),
        migrations.CreateModel(
            name='MyParticipation',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('djcollect.participation',),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='participations',
            field=models.ManyToManyField(through='djcollect.Participation', to='djuser.Subject'),
        ),
        migrations.DeleteModel(
            name='Participation',
        ),
    ]
