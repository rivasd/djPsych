'''
Created on Mar 4, 2016

@author: Daniel Rivas
'''
from djexperiments.models import Experiment


def get_my_exps(user):
    
    return Experiment.objects.filter(research_group__in=user.groups.all())