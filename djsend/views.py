"""
views.py for djsend
"""

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext as _
from djexperiments.models import Experiment

# Create your views here.

def sendSettings(request):
    
    if not request.is_ajax():
        return HttpResponseBadRequest()
    
    if not request.user.is_authenticated():
        return JsonResponse({'error': _("You must be authenticated to request an experiment.")})
    
    try:
        exp_label = request.GET['experiment']
        exp_version = request.GET['version']
    except:
        return JsonResponse({'error': _('Missing obligatory URL GET parameters, see the documentation.')})
    
    try:
        exp = Experiment.objects.get(label=exp_label)
    except Experiment.DoesNotExist:
        return JsonResponse({'error': _("There is no experiment by the name: "+exp_label)})
    
    
    
    pass