from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.utils.translation import ugettext as _
from djPsych.exceptions import SettingException, ParticipationRefused
from djuser.models import Subject
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

# Create your models here.

class BaseExperiment(models.Model):
    """
    An available experiment implemented on the site
    """
    
    class Meta:
        abstract = True
    
    label = models.CharField(max_length=32, unique=True)
    verbose_name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    estimated_length = models.CharField(max_length=16, blank=True, null=True)
    allow_repeats = models.BooleanField(help_text="Should participants be able to repeat this experiment? Does not mean they'll get payed twice, but this might create redundant data?")
    max_repeats = models.SmallIntegerField(null=True, blank=True, help_text = l_("If repeats are permitted, you can set a limit of repeats here."))
    enforce_finish = models.BooleanField(help_text=l_("Check this to prevent subjects from starting new participations when they already have incomplete ones pending."))
    max_pending = models.PositiveSmallIntegerField(blank=True, null=True, help_text=l_("If subjects are allowed to have many unfinished participations, you can set the maximum here"))
    compensated = models.BooleanField(help_text="True if some kind of monetary compensation is currently available for subjects who complete the experiment", default=False)
    max_payouts = models.IntegerField(help_text="How many times can a subject get payed (each payout needs a new participation)", blank=True, null=True)
    allow_do_overs = models.BooleanField(help_text="Should we allow subjects to erase non-claimed payments and create a better one by redoing an exp. ?", blank=True, default=False)
    funds_remaining = models.FloatField(blank=True, null=True, help_text="How much money is still available to pay subjects. This is a live setting so better to change this programmatically, ask the administrator.")
    is_active = models.BooleanField(help_text="Uncheck to remove this experiment from being displayed and served on the site.")
    
    settings_model = models.ForeignKey(ContentType)
    block_models = models.ManyToManyField(ContentType, related_name="experiments")
    research_group = models.OneToOneField(Group, null=True, blank=True)
    
    paypal_client_id=models.CharField(max_length=128, null=True, blank=True, help_text=l_("If you plan on paying your subjects via Paypal, put the client id given to you when you registered your developer account. See: https://developer.paypal.com/developer/applications/"))
    paypal_secret = models.CharField(max_length=128, null=True, blank=True, help_text=l_("The secret key given to you by PayPal"))
    ParticipationRefused = ParticipationRefused
    
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
        
    def get_global_settings(self, version, waiting=None, requested=None):
        """
        Function hook to customize the djsend.models.BaseGlobalSetting subclass to you want returned depending on the request
        Default implementation is to simply fetch the globalsetting object that has name=version. 
        
        version: the name of the requested GlobalSetting object
        waiting: either none or a queryset containing all the currently incomplete Participations
        requested: if there was a particular Participation that was requested to be completed, this is its primary key
        """
        
        return self.settings_model.get_object_for_this_type(name=version, experiment=self)
        
    def save(self, *args, **kwargs):
        
        if self.pk is None:
            new_group = Group(name=self.label+"_researchers")
            new_group.save()
            self.research_group = new_group
            exp_content_type = ContentType.objects.get_for_model(Experiment)
            exp_perm = Permission.objects.get(content_type=exp_content_type, codename="change_experiment")
            
            new_group.permissions.add(exp_perm)
            new_group.save()
        super(BaseExperiment, self).save()
        
    def create_participation(self, subject, started, complete=False):
        
        part = self.participation_model(subject=subject, experiment=self, started=started, complete=complete)
        part.save()
        return part
        
class Experiment(BaseExperiment):
    # participations = models.ManyToManyField(Subject, through='djcollect.Participation')
    
    
    pass
        

    