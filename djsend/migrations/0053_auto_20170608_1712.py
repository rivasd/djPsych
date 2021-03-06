# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-08 21:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('djsend', '0052_auto_20170410_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationCategorizationBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_settings_id', models.PositiveIntegerField(help_text='Which configuration object among your configs of the above type is this block attached to?')),
                ('name', models.CharField(help_text='A short name to describe this block', max_length=24)),
                ('position_in_timeline', models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.')),
                ('reprise', models.PositiveSmallIntegerField(blank=True, help_text="If set, indicates that this block is a reprise of the n'th block, where n is the value of the field", null=True)),
                ('length', models.PositiveIntegerField(blank=True, help_text="How many individual trials of this type should there be. You can leave blank if you don't need it", null=True)),
                ('has_practice', models.BooleanField(default=False, help_text='Check if you want to mark this block to need a practice block before, useful to guide client-side JS code.')),
                ('extra_params', jsonfield.fields.JSONField(blank=True, null=True)),
                ('timeout', models.IntegerField(default=-1, help_text='time limit for the participant before the trial automatically advances')),
                ('timeout_feedback', models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64)),
                ('timeout_feedback_en', models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64, null=True)),
                ('timeout_feedback_fr', models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64, null=True)),
                ('timeout_feedback_es', models.CharField(blank=True, help_text='Any content here will be displayed as a feedback given to the participants when he takes too long to answer the question if there is a timeout', max_length=64, null=True)),
                ('timing_fixation_cross', models.IntegerField(help_text='How long to show the fixation cross for in milliseconds.')),
                ('timing_feedback', models.IntegerField(help_text='How long to show the feedback message for in milliseconds.')),
                ('timing_stims', models.IntegerField(help_text='How long to show the stimuli for.')),
                ('timing_after', models.IntegerField(help_text='How long to leave a blank after the trial')),
                ('prompt', models.CharField(blank=True, help_text='Any content here will be displayed below the stimulus, as a reminder to the participant', max_length=256)),
                ('prompt_en', models.CharField(blank=True, help_text='Any content here will be displayed below the stimulus, as a reminder to the participant', max_length=256, null=True)),
                ('prompt_fr', models.CharField(blank=True, help_text='Any content here will be displayed below the stimulus, as a reminder to the participant', max_length=256, null=True)),
                ('prompt_es', models.CharField(blank=True, help_text='Any content here will be displayed below the stimulus, as a reminder to the participant', max_length=256, null=True)),
                ('same_key', models.CharField(blank=True, help_text='The key that the person have to press if the first image is the same as the last', max_length=3)),
                ('different_key', models.CharField(blank=True, help_text='The key that the person have to press if it is the second image that is the same as the last', max_length=3)),
                ('global_settings_type', models.ForeignKey(help_text='What kind of global configuration is this object part of?', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('save_with', models.ForeignKey(help_text="Choose the data model that will be used to save all trials that have their 'type' parameter equal to what you wrote above.     If You have different block-setting objects (like this one) that have the same 'type' but different 'save_with', then there is no guarantee which data-model will be used. This is because I think there is no real reason why two different 'categorization' blocks should be saved with different data-models: even if they have wildly different stimuli or timing settings, they should return the same kind of data.", on_delete=django.db.models.deletion.CASCADE, related_name='created_relationcategorizationblocks', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterIndexTogether(
            name='relationcategorizationblock',
            index_together=set([('global_settings_type', 'global_settings_id')]),
        ),
    ]
