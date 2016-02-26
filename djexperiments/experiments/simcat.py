'''
Created on Feb 23, 2016

@author: User
'''

from djcollect.models import Participation
from djexperiments.models import Experiment
from djsend.models import SimCatGlobalSetting

class MyParticipation(Participation):
    
    class Meta:
        proxy=True
        
class MyExperiment(Experiment):
    
    class Meta:
        proxy=True

EXPERIMENT_PROXY = MyExperiment
PARTICIPATION_PROXY = MyParticipation
GEN_SETTINGS_MODEL = SimCatGlobalSetting