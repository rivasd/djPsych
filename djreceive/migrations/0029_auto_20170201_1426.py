# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-01 19:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djreceive', '0028_auto_20170201_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audiocattrial',
            old_name='new_correct',
            new_name='correct',
        ),
        migrations.RemoveField(
            model_name='audiocattrial',
            name='old_correct',
        ),
    ]
