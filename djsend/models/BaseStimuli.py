'''
Created on Nov 02, 2016

@author: Catherine Prevost
'''

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import json

class BaseStimuli(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
class Question(BaseStimuli):
    question_label = models.CharField( max_length = 1024, help_text=l_("Question:"))
    answer_options = models.CharField( max_length = 1024, help_text=l_("Choose the labels for the possibles answers for each question. You have separate them with a coma and no spaces. ex: yes,no,maybe. Leaving a space using the likert survey will put a blank in the scale. Ex: 1,,,4"))
    required = models.BooleanField(help_text=l_("If the question is required. If so, put true, else put false."), default=False)
    
    
    def __str__(self):
        return self.question_label
        
    