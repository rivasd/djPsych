# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-03 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('djsend', '0031_remove_categorizeanimationblock_key_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeSortBlock',
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
                ('stim_height', models.PositiveIntegerField(default=100, help_text='The height of the images in pixels.')),
                ('stim_width', models.PositiveIntegerField(default=100, help_text='The width of the images in pixels.')),
                ('sort_area_height', models.PositiveIntegerField(default=800, help_text='The height of the container that subjects can move the stimuli in. Stimuli will be constrained to this area.')),
                ('sort_area_width', models.PositiveIntegerField(default=800, help_text='The width of the container that subjects can move the stimuli in. Stimuli will be constrained to this area.')),
                ('prompt', models.CharField(blank=True, help_text='The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press).', max_length=256)),
                ('prompt_en', models.CharField(blank=True, help_text='The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press).', max_length=256, null=True)),
                ('prompt_fr', models.CharField(blank=True, help_text='The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press).', max_length=256, null=True)),
                ('prompt_es', models.CharField(blank=True, help_text='The intention is that it can be used to provide a reminder about the action the subject is supposed to take (e.g. which key to press).', max_length=256, null=True)),
                ('prompt_location', models.CharField(default='above', help_text="Indicates whether to show the prompt 'above' or 'below' the sorting area.", max_length=24)),
                ('global_settings_type', models.ForeignKey(help_text='What kind of global configuration is this object part of?', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('save_with', models.ForeignKey(help_text="Choose the data model that will be used to save all trials that have their 'type' parameter equal to what you wrote above.     If You have different block-setting objects (like this one) that have the same 'type' but different 'save_with', then there is no guarantee which data-model will be used. This is because I think there is no real reason why two different 'categorization' blocks should be saved with different data-models: even if they have wildly different stimuli or timing settings, they should return the same kind of data.", on_delete=django.db.models.deletion.CASCADE, related_name='created_freesortblocks', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterIndexTogether(
            name='freesortblock',
            index_together=set([('global_settings_type', 'global_settings_id')]),
        ),
    ]