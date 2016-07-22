'''
Created on Feb 23, 2016

@author: User
'''

from djcollect.models import Participation
from djexperiments.models import Experiment
from djsend.models import SimCatGlobalSetting

class MyParticipation():
    
    def calculate_payment(self, trials=None):
        cat_trials = []
        n_correct = 0
        
        for t in trials:
            if t["trial_type"] == "categorize":
                cat_trials.append(t)
        
        for last in cat_trials[-20:]:
            if last["correct"]:
                n_correct = n_correct+1
                
        if n_correct >= 16:
            return 15.00
        else:
            return 10.00
        
        
class MyExperiment(Experiment):
    
    class Meta:
        proxy=True

EXPERIMENT_PROXY = MyExperiment
PARTICIPATION_CALCULATE = MyParticipation.calculate_payment
GEN_SETTINGS_MODEL = SimCatGlobalSetting