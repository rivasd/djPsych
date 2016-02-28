from django.db import models
from django.conf import settings
from djexperiments.models import Experiment
from djuser.models import Subject
from jsonfield import JSONField
from django.contrib.auth.models import User
from djPsych.exceptions import PayoutException

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
    
    def create_run(self, start, end, browserdict=None):
        
        run = self.experiment.run_model(participation=self, start_time=start, end_time=end)
        if browserdict is not None:
            browser = browserdict.name
            version = browserdict.version
            run.browser = browser
            run.browser_version = version
        run.save()
        return run
        
    def createPayment(self, amount, receiver=None, curr='CAD', greedy=None):
        """
        Creates a payment linked to this participation. Default currency canadian dollars
        raises exceptions on failure
        """
        if hasattr(self, 'payment'):
            raise PayoutException(_("Payment already created for this participation"))
        
        if receiver is None:
            receiver = self.subject.user.email

        payment = self.experiment.payment_model(participation=self, amount=amount, receiver=receiver)
        payment.save()
        return payment
    
    def calculate_payment(self, trials):
        return 5.00
    
class Researcher(models.Model):
    """
    An extension on the Django user model that represents users who are researchers and allowed to get data.
    
    It does look like a Django permission, but first, I have no idea how to use them, and also, it's nice to store Researcher data like institution, degree, field, etc.
    """
    
    user = models.OneToOneField(User)
    institution = models.CharField(max_length=32, blank=True, null=True)
    researchs = models.ManyToManyField(Experiment, blank=True)