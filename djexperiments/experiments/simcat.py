'''
Created on Feb 23, 2016

@author: User
'''

from django.shortcuts import render
from djexperiments.models import Experiment
from djsend.models import SimCatGlobalSetting
from djPsych.utils import fetch_files_of_type
# settings up for server-side graphics generation
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json


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
        
        if granularity > len(cat_trials):
            granularity = 1
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
        
        
        
        
        loc = ticker.MultipleLocator(granularity)
        axe.xaxis.set_major_locator(loc)
        axe.plot(ord, abs)
        
        # prettification
        if self.parameters is not None and 'difficulty' in self.parameters:
            diff = str(self.parameters['difficulty'])
        else:
            diff = 'unknown'
            
        axe.set_title('Percent correct during categorization task for subject ' + str(self.subject.id) + ' difficulty ' + diff)
        axe.set_ylabel('percentage correct')
        axe.set_xlabel('trial number')
        
        vals = axe.get_yticks()
        axe.set_yticklabels(["{:3.0f}%".format(x*100) for x in vals])
        
        canvas = FigureCanvas(fig)
        
        return canvas
        
    
class MyExperiment(Experiment):
    
    class Meta:
        proxy=True


# some views that will be used only for our lab's purposes

def texture_generator(request):
    
    # the generator will need a list of all available microcomponents, and sice it is javascript it cannot directly  get it form the server
    micro_components = fetch_files_of_type('djexperiments/static/djexperiments/simcat/attributes/', 'png')
    
    return render(request, 'djexperiments/simcat/texture-generator.html', {'microcomponents': json.dumps(micro_components)})
    pass

EXPERIMENT_PROXY = MyExperiment
PARTICIPATION_CALCULATE = MyParticipation.calculate_payment
PLOTTING = MyParticipation.learning_curve
GEN_SETTINGS_MODEL = SimCatGlobalSetting