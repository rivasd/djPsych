# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('djcollect', '__first__'),
        ('djuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=64)),
                ('label', models.CharField(max_length=32, unique=True)),
                ('verbose_name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('estimated_length', models.CharField(blank=True, max_length=16, null=True)),
                ('allow_repeats', models.BooleanField(help_text="Should participants be able to repeat this experiment? Does not mean they'll get payed twice, but this might create redundant data?")),
                ('max_repeats', models.SmallIntegerField(help_text='If repeats are permitted, you can set a limit of repeats here.')),
                ('compensated', models.BooleanField(default=False, help_text='True if some kind of monetary compensation is currently available for subjects who complete the experiment')),
                ('max_payouts', models.IntegerField(blank=True, help_text='How many times can a subject get payed (each payout needs a new participation)', null=True)),
                ('allow_do_overs', models.BooleanField(default=False, help_text='Should we allow subjects to erase non-claimed payments and create a better one by redoing an exp. ?')),
                ('funds_remaining', models.FloatField(blank=True, help_text='How much money is still available to pay subjects. This is a live setting so better to change this programmatically, ask the administrator.', null=True)),
                ('is_active', models.BooleanField(help_text='Uncheck to remove this experiment from being displayed and served on the site.')),
                ('participations', models.ManyToManyField(through='djcollect.Participation', to='djuser.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
