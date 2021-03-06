# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-09 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0047_auto_20170203_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='abxblock',
            name='prompt_position',
            field=models.IntegerField(choices=[(1, 'With the first image and until the end of the trial'), (2, 'After the three images and until the end of the trial')], default=1, help_text='When do you want the prompt to appear'),
            preserve_default=False,
        ),
    ]
