'''
Created on Oct 19, 2016

@author: rivas
'''

from django import template
from djexperiments.models import Experiment

register = template.Library()

@register.inclusion_tag("custom_tag_templates/cardify.html")
def cardify(experiment):
    return {"exp": experiment}
