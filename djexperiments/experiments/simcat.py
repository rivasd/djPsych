'''
Created on Feb 23, 2016

@author: User
'''

from djcollect.models import Participation
from djexperiments.models import Experiment
from djsend.models import SimCatGlobalSetting
# settings up for server-side graphics generation
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
        
    def learning_curve(self, granularity=1, range=20):
        
        cat_trials = [t.toDict() for t in self.get_all_trials() if t.trial_type == 'categorize']
        fig = matplotlib.figure.Figure()
        
        # our axes
        ord = []
        abs = []
        
        cur = 0
        while cur < len(cat_trials):
            lower = cur - range if (cur - range) > 0 else 0
            subset = cat_trials[lower:cur+1]
            
            average = 0.0
            for t in subset:
                if t['correct'] == True:
                    average = average+1
                    
            average = average/len(subset)
            
            
            ord.append(cur)
            abs.append(average)
            cur = cur+granularity
        
        axe = fig.add_subplot(111)
        axe.plot(ord, abs)
        canvas = FigureCanvas(fig)
        
        return canvas
        
        
class MyExperiment(Experiment):
    
    class Meta:
        proxy=True

EXPERIMENT_PROXY = MyExperiment
PARTICIPATION_CALCULATE = MyParticipation.calculate_payment
PLOTTING = MyParticipation.learning_curve
GEN_SETTINGS_MODEL = SimCatGlobalSetting