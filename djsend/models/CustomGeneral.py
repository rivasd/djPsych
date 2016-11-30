'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from .BasicGeneral import BaseGlobalSetting
from django.utils.translation import ugettext_lazy as l_
from django.conf import settings

class SimCatGlobalSetting(BaseGlobalSetting):
    sample_table_height = models.IntegerField(help_text='In the table of sample stimuli shown at the beginning, how many images hight should the table be.' )
    sample_table_width = models.IntegerField(help_text="In the table of sample stimuli shown at the beginning, how many images across should the table be.")
    levels = models.IntegerField(help_text="Starting from the easiest difficulty (all microcomponents are invariants), how many difficulty levels should be allowed? (the final difficulty will be chosen at random among the allowed levels)")
    # Stimuli creation settings
    density = models.IntegerField(help_text="how many micro components should fit along the height and width of the finished stimulus, controls how dense is the stimulus")
    size = models.PositiveIntegerField(help_text=l_("The size of the square stimuli in pixels (length of its sides)"))
    number_of_pauses = models.PositiveSmallIntegerField(default=0, help_text=l_("how many pauses with questionnaire should we insert"))
    length = models.PositiveIntegerField(help_text=l_("How many stimuli pairs should be created"), default=40)
    practices = models.PositiveIntegerField(help_text=l_("How many practice trials should be run before starting the real task"), default=5)
    difficulty = models.PositiveSmallIntegerField(default=0, blank=True, help_text=l_("If not zero, the fixed difficulty at which to run the experiment"))
    
    microcomponent_pairs = models.ManyToManyField('djstim.MicroComponentPair', related_name='settings')
    practice_pairs = models.ManyToManyField('djstim.MicroComponentPair', related_name='practice_settings')
    
    def toDict(self):
        super_dict = super(SimCatGlobalSetting, self).toDict()
        # we should add the categories and microcomponent pairs for our experiment
        microcomponents = {}
        prefix = settings.MEDIA_URL+self.experiment.label+'/attributes/'
        for pair in self.microcomponent_pairs.all():
            microcomponents[pair.index] = {
                '0': prefix+pair.first,
                '1': prefix+pair.second
            }
        
        super_dict['microcomponents'] = microcomponents
        
        practice = {}
        for pair in self.practice_pairs.all():
            practice[pair.index] = {
                '0': prefix+pair.first,
                '1': prefix+pair.second
            }
        
        super_dict['practice_components'] = practice
        
        categories = {}
        for cat in self.category_set.all():
            categories[cat.name] = cat.keycode
        
        super_dict['categories'] = categories
        return super_dict