'''
Created on Feb 23, 2016

@author: User
'''
from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from jsonfield import JSONField
from .Instructions import Instruction


class BaseSettingBlock(models.Model):
    
    class Meta:
        abstract = True
    
    global_settings_type = models.ForeignKey(ContentType)
    global_settings_id = models.PositiveIntegerField(help_text=l_("Which global settings configuration is this block-level configuration part of?"))
    part_of = GenericForeignKey('global_settings_type', 'global_settings_id')
    
    position_in_timeline = models.PositiveSmallIntegerField(null=True, blank=True, help_text=l_("This number is used by the global setting this object is part of to build its timeline. It represents the ordinal position in which this block should come."))
    reprise = models.PositiveSmallIntegerField(null=True, blank=True, help_text=l_("If set, indicates that this block is a reprise of the n'th block, where n is the value of the field"))
    length= models.PositiveIntegerField(null=True, blank=True, help_text=l_("How many individual trials of this type should there be. You can leave blank if you don't need it"))
    for_type = models.CharField(max_length=26)
    is_practice = models.BooleanField()
    instructions = GenericRelation(Instruction, )
    # magic field for dynamically added settings
    extra_params = JSONField(null=True, blank=True)
    
    def toDict(self):
        dictionary = dict(self.__dict__)
        del dictionary['_state']
        dictionary['instructions'] = self.sort_instructions()
        return dictionary
    
    def sort_instructions(self):
        instructions = {}
        instructions_before=[]
        instructions_after=[]
        for inst in self.instructions.all():
            if not inst.after:
                instructions_before.append(inst)
            else:
                instructions_after.append(inst)
        instructions_before.sort(key=lambda x:x.order)
        instructions_after.sort(key=lambda x:x.order)
        
        if instructions_after:
            instructions['after']=[]
            for instruction in instructions_after:
                instructions['after'].append(instruction.toDict())
                
        if instructions_before:
            instructions['before']=[]
            for instruction in instructions_before:
                instructions['before'].append(instruction.toDict())
        
        return instructions
        
class GenericSettingBlock(BaseSettingBlock):
    pass

