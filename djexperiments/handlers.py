'''
Created on Feb 23, 2016

@author: User
'''

from django.dispatch import receiver
from django.db.models.signals import post_init
from django.utils.translation import ugettext as _
from djPsych.exceptions import BackendConfigException
from djexperiments.models import Experiment
from djcollect.models import Participation
from importlib import import_module
@receiver(post_init, sender=Experiment)
def loadCustomModels(sender, instance, **kwargs):
    """
    Creates a way to retrieve the custom, proxy inherited models that we will need to use
    with the just created Experiment object.
    """
    
    try:
        custom_models = import_module('djexperiments.experiments.'+instance.label)
    except ImportError:
        raise BackendConfigException(_("Each experiment must have a python module present in the djexperiment.experiments package"))
    try:
        participation_proxy = custom_models.PARTICIPATION_PROXY
    except AttributeError:
        participation_proxy = Participation
    setattr(instance, 'participation_model', participation_proxy)
    # TODO: set the other class attributes!