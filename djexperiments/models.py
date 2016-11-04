# Bonjour catherine!!
# est ce que tu vois ca??
import os
from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as l_
from django.utils.translation import ugettext as _
from djPsych.exceptions import SettingException, ParticipationRefused
from djuser.models import Subject
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django_markdown.models import MarkdownField
import markdown


# Create your models here.

class BaseExperiment(models.Model):
    """
    An available experiment implemented on the site
    """
    
    class Meta:
        abstract = True
    
    label = models.CharField(max_length=32, unique=True)
    verbose_name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    estimated_length = models.CharField(max_length=16, blank=True, null=True)
    allow_repeats = models.BooleanField(help_text="Should participants be able to repeat this experiment? Does not mean they'll get payed twice, but this might create redundant data?")
    max_repeats = models.SmallIntegerField(null=True, blank=True, help_text = l_("If repeats are permitted, you can set a limit of repeats here."))
    enforce_finish = models.BooleanField(help_text=l_("Check this to prevent subjects from starting new participations when they already have incomplete ones pending."))
    max_pending = models.PositiveSmallIntegerField(blank=True, null=True, help_text=l_("If subjects are allowed to have many unfinished participations, you can set the maximum here"))
    compensated = models.BooleanField(l_('Remuneration available'), help_text="True if some kind of monetary compensation is currently available for subjects who complete the experiment", default=False)
    max_payouts = models.IntegerField(help_text="How many times can a subject get payed (each payout needs a new participation)", blank=True, null=True)
    allow_do_overs = models.BooleanField(help_text="Should we allow subjects to erase non-claimed payments and create a better one by redoing an exp. ?", blank=True, default=False)
    funds_remaining = models.FloatField(blank=True, null=True, help_text="How much money is still available to pay subjects. This is a live setting so better to change this programmatically, ask the administrator.")
    is_active = models.BooleanField(l_('Active'), help_text="Uncheck to remove this experiment from being displayed and served on the site.")
    total_funds_added = models.FloatField(blank=True, null=True, help_text="How much money have been added to this experiment since its creation")
    
    settings_model = models.ForeignKey(ContentType)
    block_models = models.ManyToManyField(ContentType, related_name="experiments")
    research_group = models.OneToOneField(Group, null=True, blank=True)
    
    PayPal_API_Username = models.CharField(max_length=64, blank=True, null=True, help_text=l_("API username for your app to access the NVP/SOAP Paypal API"))
    PayPal_API_Password = models.CharField(max_length=64, blank=True, null=True, help_text=l_("API Password for NVP/SOAP calls to Paypal"))
    PayPal_API_Signature = models.CharField(max_length=128, blank=True, null=True, help_text=l_("API Signature for NVP/SOAP calls to Paypal"))
    PayPal_Live_ID = models.CharField(max_length=64, blank=True, null=True, help_text=l_("The PayPAl Live AppID for your experiment"))
    PayPal_sender_email = models.EmailField(null=True, blank=True)
    
    ParticipationRefused = ParticipationRefused
    
    def __str__(self):
        return self.verbose_name
    

    
    
    def augmentFunds(self, boost):
        if boost <=0:
            raise SettingException(_("Cannot add negative funds to experiment"))
        
        if self.funds_remaining is not None:
            self.funds_remaining = self.funds_remaining + round(boost, 2)
            self.funds_remaining = round(self.funds_remaining, 2)
            self.total_funds_added += round(boost, 2)
            self.total_funds_added = round(self.total_funds_added, 2)
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
            os.makedirs(os.path.join(settings.MEDIA_ROOT, self.label))
        super(BaseExperiment, self).save()
        
    def create_participation(self, subject, started, complete=False, parameters={}):
        
        part = self.participation_model(subject=subject, experiment=self, started=started, complete=complete, parameters=parameters)
        part.save()
        return part
        
    def get_all_configurations(self):
        """
        Returns a list of all instances of self.settings_model that point to this experiment
        Basically it returns all the configurations of this exp, but only those that are of the type defined by this experiment's 'setting_model' field
        If you change the 'setting_model' of your experiment, then this will not return configs of the previous type, careful
        """    
        
        return self.settings_model.model_class().objects.filter(experiment=self)
    
    def count_finished_part(self):
        """
        
        """
        return self.participation_set.count()
    
    count_finished_part.short_description = l_("#Completed participations: ")
    
     
    def list_static_resources(self):
        """
        Returns dict representing the contents of the experiment's static resources directory. Limited to 1-lvl deep
        WARNING works only with local filesystem storage!!!!
        
        returns:    dict with one entry per subfolder, entry 'root' represents the top level '.'. Each entry is a list of files contained there
        """
        
        resource_dict = {'root': []}
        exp_root = os.path.join(settings.MEDIA_ROOT, self.label)
        if os.path.exists(exp_root):
            entries =  default_storage.listdir(exp_root)
        
            if entries[1]: #only write an entry if list is not empty
                resource_dict['root'] = entries[1]
                
            for folder in entries[0]:
                if  folder == 'root': 
                    folder = 'root1'
                    
                subfiles = default_storage.listdir(os.path.join(exp_root, folder)) #guard against empty directories
                if subfiles[1]:
                    resource_dict[folder] = subfiles[1]
            
            return resource_dict
        else:
            return []
        
    def is_researcher(self, request):
        """
        indicates whether the given request comes from a user that is in the research group of this experiment
        """
        
        return self.research_group in request.user.groups.all()
         
    
    def list_static_urls(self):
        resource_dict = self.list_static_resources()
        url_dict = {"js": [], "css": [], 'other':[]}
        for folder, filelist in resource_dict.items():
            directory = folder if folder != "root" else ""
            
            for file in filelist:
                path = os.path.join(default_storage.base_url, self.label+'/', directory, file)
                extension = os.path.splitext(path)[1]
                
                if extension == ".js":
                    url_dict['js'].append(path)
                elif extension == '.css':
                    url_dict['css'].append(path)
                else :
                    url_dict['other'].append(path)
                
                                
        return url_dict
            
            
    
    
    
class Experiment(BaseExperiment):
    participations = models.ManyToManyField(Subject, through='djcollect.Participation')
    
    def amount_spent(self):
        total = 0.00
        for part in self.participation_set.all():
            total = total + part.payment.amount
    
        return total
        
class Debrief(models.Model):
    
    experiment = models.OneToOneField(Experiment)
    content = MarkdownField(help_text=l_("write the debrief content you'd like to show to subjects after the experiment."))
    
    def render(self):
        if self.content is not None:
            return markdown.markdown(self.content)
        else:
            return l_("No debrief information has been set by the experimenters")
        
    def __str__(self):
        return l_("Debrief for %s") % self.experiment.verbose_name

class Lobby(models.Model):
    
    experiment=models.OneToOneField(Experiment)
    content = MarkdownField(help_text=l_("Write here the content that people will see on the homepage of the experiment, before choosing to do it or not"))
    
    def render(self):
        if self.content is not None:
            return markdown.markdown(self.content)
        else:
            return l_("No homepage information has been set by the experimenters")
        
    def __str__(self):
        return l_("Welcome page for %s") % self.experiment.verbose_name
        
        