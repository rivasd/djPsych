# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-08 01:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('djexperiments', '0006_debrief_experiment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', django_markdown.models.MarkdownField(help_text='Write here the content that people will see on the homepage of the experiment, before choosing to do it or not')),
                ('content_en', django_markdown.models.MarkdownField(help_text='Write here the content that people will see on the homepage of the experiment, before choosing to do it or not', null=True)),
                ('content_fr', django_markdown.models.MarkdownField(help_text='Write here the content that people will see on the homepage of the experiment, before choosing to do it or not', null=True)),
                ('content_es', django_markdown.models.MarkdownField(help_text='Write here the content that people will see on the homepage of the experiment, before choosing to do it or not', null=True)),
                ('experiment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='djexperiments.Experiment')),
            ],
        ),
    ]