# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-04 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djexperiments', '0002_experiment_participations'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='description_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='description_fr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='verbose_name_en',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='verbose_name_es',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='verbose_name_fr',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='compensated',
            field=models.BooleanField(default=False, help_text='True if some kind of monetary compensation is currently available for subjects who complete the experiment', verbose_name='Remuneration available'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='is_active',
            field=models.BooleanField(help_text='Uncheck to remove this experiment from being displayed and served on the site.', verbose_name='Active'),
        ),
    ]
