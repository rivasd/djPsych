from django.db import models
from django.conf import settings
from djexperiments.models import Experiment
from djuser.models import Subject
from jsonfield import JSONField
from django.contrib.auth.models import User
from djPsych.exceptions import PayoutException
from djreceive.models import Run
from matplotlib import ticker, figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Create your models here.

class Participation(models.Model):
    """
    Represents a single participation of a Subject to an Experiment
    
    Meant to hold multiple Run objects, allows a participation to be completed in different attempts
    I recommend to always get a Participation instance with select_related()
    """
    
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    complete = models.BooleanField()
    started = models.DateTimeField()
    # browser = models.CharField(max_length=64)
    finished = models.DateTimeField(null=True, blank=True)
    #this is where the magic happens: store options in json format here so that experimental settings stay the same across sessions
    parameters = JSONField(null=True, blank=True)
    
    def create_run(self, start, end, setting=None, browserdict=None):
        
        run = Run(participation=self, start_time=start, global_setting_obj=setting, end_time=end)
        if browserdict is not None:
            browser = browserdict['name']
            version = browserdict['version']
            run.browser = browser
            run.browser_version = version
        run.save()
        return run
        
    def create_payment(self, trials=None, receiver=None, curr='CAD', greedy=None):
        """
        Creates a payment linked to this participation. Default currency canadian dollars
        raises exceptions on failure
        """
        if hasattr(self, 'payment'):
            raise PayoutException(_("Payment already created for this participation"))
        
        if receiver is None:
            receiver = self.subject.user.email

        payment = self.experiment.payment_model(participation=self, amount=self.calculate_payment(trials), receiver=receiver)
        payment.save()
        return payment
    
    def calculate_payment(self, trials=None):
        if trials is None:
            trials = self.get_all_trials()
        
        return 5.00
    
    def get_all_trials(self):
        trial_list = []
        for run in self.run_set.all().order_by("start_time"):
            for trial in run.get_trials():
                trial_list.append(trial)
        return trial_list
    
    def get_headers(self):
        header_set = set()
        for trial in self.get_all_trials():
            header_set = header_set.union(trial.get_full_field_names())
        return list(header_set)
    
    def get_data_as_dict_array(self):
        dict_array=[]
        for trial in self.get_all_trials():
            dict_array.append(trial.toDict())
            
        return dict_array
    
    def completion_status(self):
        """
        Returns a dict that describes how many runs of each kind have been completed and linked to this part. 
        Runs are organized by the name of the GlobalSetting that was used when the subject generated the data
        
        returns false for runs saved before implementation of  this feature
        """
        runs = {}
        for run in self.run_set.all():
            
            if run.global_setting_obj is not None:
                if hasattr(runs, run.global_setting_obj.name): #TODO: this is not backwards compatible. FIX IT
                    runs[run.global_setting_obj.name] += 1
                else:
                    runs[run.global_setting_obj.name] = 1
            
            else:
                return False
        return runs

    def __str__(self):
        return self.subject.user.username+" - "+self.experiment.label

    def learning_curve(self, granularity=1, range=20):
        
        cat_trials = [t.toDict() for t in self.get_all_trials() if (t.trial_type == 'categorize' or t.trial_type == 'audio-categorization')]
        fig = figure.Figure()
        
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
                if t['correct'] == True or t['correct'] == "correct":
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

class DropOut(models.Model):
    
    """
    Represents a single unfinished participation of a subject to an experiment   
    
    """
    
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    started = models.DateTimeField()
    finished = models.DateTimeField(null=True, blank=True)

    
    
class Researcher(models.Model):
    """
    An extension on the Django user model that represents users who are researchers and allowed to get data.
    
    It does look like a Django permission, but first, I have no idea how to use them, and also, it's nice to store Researcher data like institution, degree, field, etc.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=32, blank=True, null=True)
    researchs = models.ManyToManyField(Experiment, blank=True)