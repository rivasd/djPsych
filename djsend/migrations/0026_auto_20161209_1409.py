# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-09 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('djsend', '0025_auto_20161207_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyTextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_settings_id', models.PositiveIntegerField(help_text='Which configuration object among your configs of the above type is this block attached to?')),
                ('name', models.CharField(help_text='A short name to describe this block', max_length=24)),
                ('position_in_timeline', models.PositiveSmallIntegerField(blank=True, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.', null=True)),
                ('reprise', models.PositiveSmallIntegerField(blank=True, help_text="If set, indicates that this block is a reprise of the n'th block, where n is the value of the field", null=True)),
                ('length', models.PositiveIntegerField(blank=True, help_text="How many individual trials of this type should there be. You can leave blank if you don't need it", null=True)),
                ('type', models.CharField(help_text="This will be passed as the 'type' parameter to jsPsych. It tells it which plugin to use to render these trials.", max_length=26)),
                ('has_practice', models.BooleanField(default=False, help_text='Check if you want to mark this block to need a practice block before, useful to guide client-side JS code.')),
                ('extra_params', jsonfield.fields.JSONField(blank=True, null=True)),
                ('preamble', models.TextField(blank=True, help_text='A short paragraphe that will display at the top of your questions page', null=True)),
                ('preamble_en', models.TextField(blank=True, help_text='A short paragraphe that will display at the top of your questions page', null=True)),
                ('preamble_fr', models.TextField(blank=True, help_text='A short paragraphe that will display at the top of your questions page', null=True)),
                ('preamble_es', models.TextField(blank=True, help_text='A short paragraphe that will display at the top of your questions page', null=True)),
                ('global_settings_type', models.ForeignKey(help_text='What kind of global configuration is this object part of?', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('save_with', models.ForeignKey(help_text="Choose the data model that will be used to save all trials that have their 'type' parameter equal to what you wrote above.     If You have different block-setting objects (like this one) that have the same 'type' but different 'save_with', then there is no guarantee which data-model will be used. This is because I think there is no real reason why two different 'categorization' blocks should be saved with different data-models: even if they have wildly different stimuli or timing settings, they should return the same kind of data.", on_delete=django.db.models.deletion.CASCADE, related_name='created_surveytextblocks', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_options',
            field=models.CharField(blank=True, help_text='Only for likert and multi-choices surveys!!! Choose the labels for the possibles answers for each question. You have separate them with a coma and no spaces. ex: yes,no,maybe. Leaving a space using the likert survey will put a blank in the scale. Ex: 1,,,4', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_options_en',
            field=models.CharField(blank=True, help_text='Only for likert and multi-choices surveys!!! Choose the labels for the possibles answers for each question. You have separate them with a coma and no spaces. ex: yes,no,maybe. Leaving a space using the likert survey will put a blank in the scale. Ex: 1,,,4', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_options_es',
            field=models.CharField(blank=True, help_text='Only for likert and multi-choices surveys!!! Choose the labels for the possibles answers for each question. You have separate them with a coma and no spaces. ex: yes,no,maybe. Leaving a space using the likert survey will put a blank in the scale. Ex: 1,,,4', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_options_fr',
            field=models.CharField(blank=True, help_text='Only for likert and multi-choices surveys!!! Choose the labels for the possibles answers for each question. You have separate them with a coma and no spaces. ex: yes,no,maybe. Leaving a space using the likert survey will put a blank in the scale. Ex: 1,,,4', max_length=1024, null=True),
        ),
        migrations.AlterIndexTogether(
            name='surveytextblock',
            index_together=set([('global_settings_type', 'global_settings_id')]),
        ),
    ]
