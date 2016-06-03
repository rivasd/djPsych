# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-06 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0006_auto_20160306_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='css_class',
            field=models.CharField(blank=True, default='', help_text="All instructions are rendered inside an HTML 'p' element with a class attribute 'instructions'. You can add to the class attribute here.", max_length=64, null=True),
        ),
    ]