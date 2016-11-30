from django.db import models
from django.conf import settings
from djexperiments.models import Experiment
from djuser.models import Subject
from jsonfield import JSONField
from django.contrib.auth.models import User
from djPsych.exceptions import PayoutException
from djreceive.models import Run

# Create your models here.

class Participation(models.Model):
    """
    Represents a single participation of a Subject to an Experiment
    
    Meant to hold multiple Run objects, allows a participation to be completed in different attempts
    I recommend to always get a Participation instance with select_related()
    """
    
    experiment = models.ForeignKey(Experiment)
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
        
        """
        runs = {}
        for run in self.run_set.all():
            if hasattr(runs, run.global_setting_obj.name):
                runs[run.global_setting_obj.name] += 1
            else:
                runs[run.global_setting_obj.name] = 1
        
        return runs

class DropOut(models.Model):
    
    """
    Represents a single unfinished participation of a subject to an experiment   
    
    """
    
    experiment = models.ForeignKey(Experiment)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    started = models.DateTimeField()
    finished = models.DateTimeField(null=True, blank=True)

    
    
class Researcher(models.Model):
    """
    An extension on the Django user model that represents users who are researchers and allowed to get data.
    
    It does look like a Django permission, but first, I have no idea how to use them, and also, it's nice to store Researcher data like institution, degree, field, etc.
    """
    
    user = models.OneToOneField(User)
    institution = models.CharField(max_length=32, blank=True, null=True)
    researchs = models.ManyToManyField(Experiment, blank=True)