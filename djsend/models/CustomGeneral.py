'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from .BasicGeneral import GlobalSetting


class SimCatGlobalSetting(GlobalSetting):
    sample_table_height = models.IntegerField(help_text='In the table of sample stimuli shown at the beginning, how many images hight should the table be.' )
    sample_table_width = models.IntegerField(help_text="In the table of sample stimuli shown at the beginning, how many images across should the table be.")
    levels = models.IntegerField(help_text="Starting from the easiest difficulty (all microcomponents are invariants), how many difficulty levels should be allowed? (the final difficulty will be chosen at random among the allowed levels)")
    # Stimuli creation settings
    density = models.IntegerField(help_text="how many micro components should fit along the height and width of the finished stimulus, controls how dense is the stimulus")