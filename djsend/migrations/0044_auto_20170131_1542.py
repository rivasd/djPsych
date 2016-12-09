# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-31 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djsend', '0043_auto_20170127_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiocatblock',
            name='forced_listening',
            field=models.BooleanField(default=False, help_text='Check this box if you want to force the subject to listen to the whole sound before answering'),
        ),
        migrations.AlterField(
            model_name='animationblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='audioabxblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='audiocatblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='audiosimilarityblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='buttonresponseblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='categorizationblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='categorizeanimationblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='forcedchoiceblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='freesortblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='genericsettingblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='htmlblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='multistimmultiresponseblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='ratingblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='reconstructionblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='samedifferentblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='similarityblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='singleaudioblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='singlestimblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='surveylikertblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='surveymultichoiceblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='surveytextblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
        migrations.AlterField(
            model_name='xabblock',
            name='position_in_timeline',
            field=models.PositiveSmallIntegerField(default=0, help_text='This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come.'),
        ),
    ]