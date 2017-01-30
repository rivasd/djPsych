'''
Created on Oct 19, 2016

@author: rivas
'''

from django import template

register = template.Library()

@register.inclusion_tag("custom_tag_templates/cardify.html")
def cardify(experiment, request):
    is_researcher = experiment.is_researcher(request)
    if experiment.get_latest_pending(request) and experiment.enforce_finish:
        force_cont = True
    else:
        force_cont = False
    return {"exp": experiment, 'is_researcher':is_researcher, 'force_cont': force_cont}
