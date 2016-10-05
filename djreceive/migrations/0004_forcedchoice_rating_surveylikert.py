# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-04 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djreceive', '0003_auto_20160721_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForcedChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_node_id', models.CharField(max_length=24)),
                ('trial_index', models.IntegerField()),
                ('trial_type', models.CharField(max_length=32)),
                ('time_elapsed', models.IntegerField()),
                ('timeout', models.BooleanField(default=False)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('rt', models.PositiveIntegerField()),
                ('chosen', models.CharField(max_length=128)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreceive.Run')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_node_id', models.CharField(max_length=24)),
                ('trial_index', models.IntegerField()),
                ('trial_type', models.CharField(max_length=32)),
                ('time_elapsed', models.IntegerField()),
                ('timeout', models.BooleanField(default=False)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('rt', models.PositiveIntegerField()),
                ('rating', models.IntegerField()),
                ('stimulus', models.CharField(max_length=128)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreceive.Run')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyLikert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_node_id', models.CharField(max_length=24)),
                ('trial_index', models.IntegerField()),
                ('trial_type', models.CharField(max_length=32)),
                ('time_elapsed', models.IntegerField()),
                ('timeout', models.BooleanField(default=False)),
                ('extra_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('rt', models.PositiveIntegerField()),
                ('responses', models.TextField()),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreceive.Run')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]