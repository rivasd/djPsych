# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorizationBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_settings_id', models.PositiveIntegerField(help_text='Which global settings configuration is this block-level configuration part of?')),
                ('length', models.PositiveIntegerField(blank=True, help_text="How many individual trials of this type should there be. You can leave blank if you don't need it", null=True)),
                ('for_type', models.CharField(max_length=26)),
                ('is_practice', models.BooleanField()),
                ('extra_params', jsonfield.fields.JSONField()),
                ('show_stim_with_feedback', models.BooleanField(default=False, help_text='Should the stimulus be shown together with the feedback text?')),
                ('show_feedback_on_timeout', models.BooleanField(default=False, help_text='Should we show the feedback even when the trial times out?')),
                ('timing_stim', models.IntegerField(help_text='How long to show the stimulus for (milliseconds). If -1, then the stimulus is shown until a response is given.')),
                ('timing_feedback_duration', models.IntegerField(help_text='How long to show the feedback for ')),
                ('timing_response', models.IntegerField(help_text='The maximum time allowed for a response. If -1, then the experiment will wait indefinitely for a response.')),
                ('timing_post_trial', models.IntegerField(help_text='Sets the time, in milliseconds, between the current trial and the next trial.')),
                ('global_settings_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('keycode', models.IntegerField(help_text='The character keycode representing the correct response for this category. See: http://www.cambiaresearch.com/articles/15/javascript-key-codes')),
                ('block_id', models.PositiveIntegerField(help_text='The block-level setting this category is attached to')),
                ('block_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='GenericGlobalSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="An identifier for this set of settings, for example 'production' or 'test settings' ", max_length=16, unique=True)),
                ('max_consecutive_timeouts', models.IntegerField(help_text='The experiment will automatically abort if this number if the subject does not respond fast enough to this many consecutive trials')),
                ('max_total_timeouts', models.IntegerField(help_text='The experiment will automatically abort if this many trials are allowed to timeout in total')),
                ('fixation_cross', models.CharField(help_text='The path to fixation cross image, will be appended to static/your_app_name/', max_length=32)),
                ('extra_parameters', jsonfield.fields.JSONField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericSettingBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_settings_id', models.PositiveIntegerField(help_text='Which global settings configuration is this block-level configuration part of?')),
                ('length', models.PositiveIntegerField(blank=True, help_text="How many individual trials of this type should there be. You can leave blank if you don't need it", null=True)),
                ('for_type', models.CharField(max_length=26)),
                ('is_practice', models.BooleanField()),
                ('extra_params', jsonfield.fields.JSONField()),
                ('global_settings_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericSingleStimuli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A simple name for this particular stimuli pair', max_length=26)),
                ('stimulus', models.CharField(help_text='The path to your stimuli file inside the static files folder we provided. Or it can be a short HTML string', max_length=256)),
                ('block_id', models.PositiveIntegerField()),
                ('block_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericStimuliPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A simple name for this particular stimuli pair', max_length=26)),
                ('stimulus', models.CharField(help_text='The path to your stimuli file inside the static files folder we provided. Or it can be a short HTML string', max_length=256)),
                ('block_id', models.PositiveIntegerField()),
                ('second_stim', models.CharField(help_text='The path to your stimuli file inside the static files folder we provided. Or it can be a short HTML string', max_length=256)),
                ('block_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='content_type')),
                ('is_html', models.BooleanField(help_text='check this if the content of the instruction text is valid html and wish to have it rendered as such. ')),
                ('text', models.TextField(help_text='Write your instruction page here! it can even be valid html!')),
                ('order', models.PositiveIntegerField(help_text='if a setting has multiple instruction pages, we use this number to sort the order in which you want them presented.')),
                ('after', models.BooleanField(help_text='check if this instruction page is meant to be shown AFTER the task it is attached to.')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='SimCatGlobalSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="An identifier for this set of settings, for example 'production' or 'test settings' ", max_length=16, unique=True)),
                ('max_consecutive_timeouts', models.IntegerField(help_text='The experiment will automatically abort if this number if the subject does not respond fast enough to this many consecutive trials')),
                ('max_total_timeouts', models.IntegerField(help_text='The experiment will automatically abort if this many trials are allowed to timeout in total')),
                ('fixation_cross', models.CharField(help_text='The path to fixation cross image, will be appended to static/your_app_name/', max_length=32)),
                ('extra_parameters', jsonfield.fields.JSONField(null=True)),
                ('sample_table_height', models.IntegerField(help_text='In the table of sample stimuli shown at the beginning, how many images hight should the table be.')),
                ('sample_table_width', models.IntegerField(help_text='In the table of sample stimuli shown at the beginning, how many images across should the table be.')),
                ('levels', models.IntegerField(help_text='Starting from the easiest difficulty (all microcomponents are invariants), how many difficulty levels should be allowed? (the final difficulty will be chosen at random among the allowed levels)')),
                ('density', models.IntegerField(help_text='how many micro components should fit along the height and width of the finished stimulus, controls how dense is the stimulus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SimilarityBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_settings_id', models.PositiveIntegerField(help_text='Which global settings configuration is this block-level configuration part of?')),
                ('length', models.PositiveIntegerField(blank=True, help_text="How many individual trials of this type should there be. You can leave blank if you don't need it", null=True)),
                ('for_type', models.CharField(max_length=26)),
                ('is_practice', models.BooleanField()),
                ('extra_params', jsonfield.fields.JSONField()),
                ('intervals', models.IntegerField(help_text='How many different choices are available on the slider. For example, 5 will limit the options to 5 different places on the slider')),
                ('show_ticks', models.BooleanField(help_text='If true, then the slider will have tick marks indicating where the response options lie on the slider.')),
                ('show_response', models.CharField(choices=[('FIRST_STIMULUS', 'With the first stimulus'), ('SECOND_STIMULUS', 'With the second stimulus'), ('POST_STIMULUS', 'After both stimuli have disappeared')], help_text='When should the response slider be shown?', max_length=16)),
                ('timing_first_stim', models.IntegerField(help_text='How long to show the first stimulus for in milliseconds.')),
                ('timing_second_stim', models.IntegerField(help_text='How long to show the second stimulus for in milliseconds. -1 will show the stimulus until a response is made by the subject.')),
                ('timing_image_gap', models.IntegerField(help_text='How long to show a blank screen in between the two stimuli.')),
                ('timing_post_trial', models.IntegerField(help_text='Sets the time, in milliseconds, between the current trial and the next trial.')),
                ('prompt', models.CharField(blank=True, help_text='Any content here will be displayed below the stimulus, as a reminder to the participant', max_length=32)),
                ('global_settings_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
