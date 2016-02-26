"""
views.py for djsend
"""

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext as _
from djexperiments.models import Experiment
from djPsych.exceptions import ParticipationRefused

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
    
    participations = exp.participation_model.objects.filter(subject__user=request.user, experiment=exp)
    len(participations.filter) # force evaluation of queryset
    previous = participations.filter(completed=True)
    on_the_ice = participations.filter(completed=False)
    
    try:
        if not hasattr(request.session, 'continue'):
            to_be_continued = None
            # special checks for brand new participations
            if on_the_ice.count() > 0 and exp.enforce_finish:
                raise ParticipationRefused(_("This experiment does not allow you to start a new participation while you have an unifinished one."))
            if on_the_ice.count() >= exp.max_pending:
                raise ParticipationRefused(_("You have reached the maximum number of unfinished participations for this experiment. Go finish one instead."))
        else:
            to_be_continued = on_the_ice.get(pk=request.session.get('continue'))
            if on_the_ice.count() > exp.max_pending:
                raise ParticipationRefused(_("You have reached the maximum number of unfinished participations for this experiment. Go finish one instead."))
        
        if previous.count() >= exp.max_repeats: # the completion of this participation would lead to too many participations
            raise ParticipationRefused(_("You have reached the maximum number of participations to this experiment."))
        if previous.count() > 0 and exp.allow_repeats:
            raise ParticipationRefused(_("Sorry! You can only do this experiment once."))
    except ParticipationRefused as e:
        return JsonResponse({'error': str(e)})
    
    global_settings_obj = exp.get_global_settings(exp_version, waiting=on_the_ice, requested=to_be_continued)
    global_settings_obj.build_timeline()
    
    
    pass