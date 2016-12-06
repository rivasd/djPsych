# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-24 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djreceive', '0007_auto_20161118_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioCatTrial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_node_id', models.CharField(max_length=24)),
                ('trial_index', models.IntegerField()),
                ('trial_type', models.CharField(max_length=32)),
                ('time_elapsed', models.IntegerField()),
                ('timeout', models.BooleanField(default=False)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('stimulus', models.CharField(max_length=128)),
                ('correct', models.BooleanField()),
                ('category', models.CharField(max_length=24, null=True)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreceive.Run')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
