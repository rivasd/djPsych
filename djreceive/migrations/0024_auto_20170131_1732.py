# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-31 22:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djreceive', '0023_audioabxtrial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audiocattrial',
            old_name='result',
            new_name='correct',
        ),
    ]
