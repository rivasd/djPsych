# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-03 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('djcollect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('currency', models.CharField(default='CAD', max_length=3)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_sent', models.DateTimeField(blank=True, null=True)),
                ('sent', models.BooleanField(default=False)),
                ('payout_item_id', models.CharField(blank=True, max_length=16, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=20, null=True)),
                ('payout_batch_id', models.CharField(blank=True, max_length=16, null=True)),
                ('time_processed', models.DateTimeField(blank=True, null=True)),
                ('receiver', models.EmailField(max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=16)),
                ('participation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='djcollect.Participation')),
            ],
        ),
    ]
