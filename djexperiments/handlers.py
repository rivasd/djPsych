'''
Created on Feb 23, 2016

@author: User
'''

from django.dispatch import receiver
from django.db.models.signals import post_init, post_save
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext as _
from djPsych.exceptions import BackendConfigException
from djexperiments.models import Experiment
from djcollect.models import Participation
from djreceive.models import Run
from djpay.models import Payment
from djsend.models import GenericGlobalSetting
from importlib import import_module
from django.contrib.contenttypes.models import ContentType

@receiver(post_init, sender=Experiment)
def loadCustomModels(sender, instance, **kwargs):
    """
    Creates a way to retrieve the custom, proxy inherited models that we will need to use
    with the just created Experiment object.
    """
    
    if instance.pk is None: #turns out the admin creates a blank instance the moment you open the object creation form... this seems kinda dumb
        return
    
    try:
        custom_models = import_module('djexperiments.experiments.'+instance.label)
    except ImportError:
        pass
        # raise BackendConfigException(_("Each experiment must have a python module present in the djexperiment.experiments package"))
    try:
        custom_calculate = custom_models.PARTICIPATION_CALCULATE
        plot = custom_models.PLOTTING
        Participation.calculate_payment = custom_calculate
        Participation.learning_curve = plot
    except:
        pass
    setattr(instance, 'participation_model', Participation)
    
    if hasattr(custom_models, 'GEN_SETTINGS_MODEL'):
        gen_set_mod = custom_models.GEN_SETTINGS_MODEL
    else:
        gen_set_mod = GenericGlobalSetting
    setattr(instance, 'global_settings_model', gen_set_mod)
    
    if hasattr(custom_models, 'RUN_MODEL'):
        run_mod = custom_models.RUN_MODEL
    else:
        run_mod = Run
    setattr(instance, 'run_model', run_mod)
    
    if hasattr(custom_models, 'PAYMENT_MODEL'):
        pay_mod = custom_models.PAYMENT_MODEL
    else:
        pay_mod = Payment
    setattr(instance, 'payment_model', pay_mod)
    
    #if hasattr(custom_models, 'EXPERIMENT_PROXY'):
    #   instance.__class__ = custom_models.EXPERIMENT_PROXY # yes this is sacrilegious, but dammit, I get results
    # TODO: set the other class attributes!
    

        
    