# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-30 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djstim', '0005_auto_20160414_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microcomponentpair',
            name='first',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='microcomponentpair',
            name='second',
            field=models.CharField(max_length=128),
        ),
    ]
