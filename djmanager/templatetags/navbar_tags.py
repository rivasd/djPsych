from django import template
from djexperiments.models import Experiment

register = template.Library()

@register.inclusion_tag('includes/researcher_navbar.html', takes_context=True)
def show_experiments(context):
    
    experiments = Experiment.objects.filter(research_group__in = context['request'].user.groups.all())
    return {'experiments': experiments}

