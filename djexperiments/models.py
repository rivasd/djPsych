from django.db import models
from django.utils.translation import ugettext_lazy as l_
from djPsych.exceptions import SettingException
from djuser.models import Subject
from jsonfield import JSONField
# Create your models here.

class BaseExperiment(models.Model):
    """
    An available experiment implemented on the site
    """
    
    class Meta:
        abstract = True
    
    app_name = models.CharField(max_length=64)
    label = models.CharField(max_length=32, unique=True)
    verbose_name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    estimated_length = models.CharField(max_length=16, blank=True, null=True)
    allow_repeats = models.BooleanField(help_text="Should participants be able to repeat this experiment? Does not mean they'll get payed twice, but this might create redundant data?")
    max_repeats = models.SmallIntegerField(help_text = l_("If repeats are permitted, you can set a limit of repeats here."))
    compensated = models.BooleanField(help_text="True if some kind of monetary compensation is currently available for subjects who complete the experiment", default=False)
    max_payouts = models.IntegerField(help_text="How many times can a subject get payed (each payout needs a new participation)", blank=True, null=True)
    allow_do_overs = models.BooleanField(help_text="Should we allow subjects to erase non-claimed payments and create a better one by redoing an exp. ?", blank=True, default=False)
    funds_remaining = models.FloatField(blank=True, null=True, help_text="How much money is still available to pay subjects. This is a live setting so better to change this programmatically, ask the administrator.")
    is_active = models.BooleanField(help_text="Uncheck to remove this experiment from being displayed and served on the site.")
    
    def __str__(self):
        return self.verbose_name
    
    def augmentFunds(self, boost):
        if boost <=0:
            raise SettingException(_("Cannot add negative funds to experiment"))
        
        if self.funds_remaining is not None:
            self.funds_remaining = self.funds_remaining + round(boost, 2)
            self.funds_remaining = round(self.funds_remaining, 2)
            self.save()
        else:
            raise SettingException(_("cannot add funds to an unfunded experiment"))
        
    def deductFunds(self, amount):
        if amount <=0:
            raise SettingException(_("Cannot subtract negative funds from experiment"))
        
        if self.funds_remaining is not None:
            self.funds_remaining = self.funds_remaining - amount if self.funds_remaining - amount > 0.0 else 0.0
            self.funds_remaining = round(self.funds_remaining, 2)
            self.save()
        else:
            raise SettingException(_("cannot subtract funds from an unfunded experiment"))
        
    def get_participations(self, user):
        """
        Given a django.contrib.auth.models.User, return the next Participation to operate on.
        
        If there is an incomplete Participation, return that one. If there are none, create a new one and return it. If the user has reached the limit of repeats, return False
        """
        participations = self.participation_model.objects.filter(subject__user=user, experiment=self)
        previous = len(participations) # force evaluation of queryset
        
        if previous >= self.max_repeats:
            return False
        
class Experiment(BaseExperiment):
    participations = models.ManyToManyField(Subject, through='djcollect.Participation')
    
    
    pass
        

    
    