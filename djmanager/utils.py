'''
Created on Mar 2, 2016

@author: Daniel
'''
from djexperiments.models import Experiment
from django.contrib.contenttypes.models import ContentType
import inspect


def content_type_is_subclass_of(ct, masterclass):
    """
    This simple method is part of a mega hack to limit the choices on ContentType fields
    """
    actual_model = ct.model_class()
    return issubclass(actual_model, masterclass)
    
def get_allowed_exp_for_user(request):
    """
    Returns a QuerySet of all Experiments accessible to the user associated with this request
    """
    research_groups = request.user.groups.filter(name__endswith='researchers')
    return Experiment.objects.filter(research_group__in=research_groups)

def get_subclass_ct_pk(baseclass):
    """
    Given a base class, returns a list of all ContentType objects whose associated model are subclasses of the baseclass.
    """
    cts =[]
    for ct in ContentType.objects.all():
            if inspect.isclass(ct.model_class()) and issubclass(ct.model_class(), baseclass):
                cts.append(ct.pk)
    return cts
