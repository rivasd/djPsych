# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-04 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djreceive', '0019_singleaudiotrial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleStimTrial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_node_id', models.CharField(max_length=24)),
                ('trial_index', models.IntegerField()),
                ('trial_type', models.CharField(max_length=32)),
                ('time_elapsed', models.IntegerField()),
                ('timeout', models.BooleanField(default=False)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('stimulus', models.CharField(max_length=128)),
                ('key_press', models.IntegerField()),
                ('rt', models.IntegerField()),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreceive.Run')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
