'''
Created on Oct 19, 2016

@author: rivas
'''

from django import template

register = template.Library()

@register.inclusion_tag("custom_tag_templates/cardify.html")
def cardify(experiment, request):
    is_researcher = experiment.is_researcher(request)
    return {"exp": experiment, 'is_researcher':is_researcher}
