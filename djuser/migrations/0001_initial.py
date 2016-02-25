# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 18:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'male'), ('F', 'female'), ('O', 'other')], max_length=1, null=True)),
                ('occupation', models.CharField(blank=True, choices=[('ft-student', 'full-time student'), ('ft-work', 'full-time work'), ('pt-student&work', 'part-time student & part-time work'), ('ft-student&pt-work', 'full-time student & part-time work')], max_length=32, null=True)),
                ('years_of_schooling', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
