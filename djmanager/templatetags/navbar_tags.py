from django import template
from djexperiments.models import Experiment

register = template.Library()

@register.inclusion_tag('researcher_navbar.html')
def show_experiments(request):
    
    experiments = Experiment.objects.filter(research_group__in = request.user.groups.all())
    
    return {'experiments': experiments}

