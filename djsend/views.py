"""
views.py for djsend
"""

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext as _
from djexperiments.models import Experiment
from djPsych.exceptions import ParticipationRefused
import random
import string
import datetime
import json
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from djreceive.models.CustomTrials import CogComHTMLTrial


# Create your views here.

def sendSettings(request, exp_label):
    
    if not request.is_ajax():
        # return HttpResponseBadRequest() #Uncomment for production
        pass
    
    if not request.user.is_authenticated():
        return JsonResponse({'error': _("You must be authenticated to request an experiment.")})
    
    try:
        exp_version = request.GET['version']
    except:
        return JsonResponse({'error': _('Missing obligatory URL GET parameters, see the documentation.')})
    
    try:
        exp = Experiment.objects.get(label=exp_label)
    except Experiment.DoesNotExist:
        return JsonResponse({'error': _("There is no experiment by the name: "+exp_label)})
    
    participations = exp.participation_model.objects.filter(subject__user=request.user, experiment=exp)
    len(participations) # force evaluation of queryset
    previous = participations.filter(complete=True)
    on_the_ice = participations.filter(complete=False)
    
    try:
        if not hasattr(request.session, 'continue'):
            to_be_continued = None
            # special checks for brand new participations
            if on_the_ice.count() > 0 and exp.enforce_finish:
                raise ParticipationRefused(_("This experiment does not allow you to start a new participation while you have an unifinished one."))
            if exp.max_pending is not None and on_the_ice.count() >= exp.max_pending:
                raise ParticipationRefused(_("You have reached the maximum number of unfinished participations for this experiment. Go finish one instead."))
        else:
            to_be_continued = on_the_ice.get(pk=request.session.get('continue')) 
            if exp.max_pending is not None and on_the_ice.count() > exp.max_pending:
                raise ParticipationRefused(_("You have reached the maximum number of unfinished participations for this experiment. Go finish one instead."))
        
        if exp.max_repeats is not None and previous.count() >= exp.max_repeats: # the completion of this participation would lead to too many participations
            raise ParticipationRefused(_("You have reached the maximum number of participations to this experiment."))
        if previous.count() > 0 and not exp.allow_repeats:
            raise ParticipationRefused(_("Sorry! You can only do this experiment once."))
    except ParticipationRefused as e:
        return JsonResponse({'error': str(e)})
    try:
        global_settings_obj = exp.get_global_settings(exp_version, waiting=on_the_ice, requested=to_be_continued)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    global_settings_obj.build_timeline(global_settings_obj.get_all_blocks(), request)
    final_settings = global_settings_obj.toDict()
    # add the subject_id to the response
    final_settings['subject'] = request.user.subject.id
    # the primary key of the participation to continue if this is a request to continue a previous participation. False otherwise
    final_settings['previous']= to_be_continued if to_be_continued is not None else False
    # generate 8 character random sequence to identify this request for an experiment. Make the session remember it, too!
    request.session['exp_id'] = final_settings['exp_id'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    request.session['current_exp'] = final_settings['current_exp'] = exp_label
    request.session['start_time'] = str(datetime.datetime.now())
    save_dict= {}
    # save a mapping of 'type' attribute to content type id so that later we know with which model to save data-objects of each type
    for block in final_settings['timeline']:
        if 'save_with_id' in block:
            save_dict[block['type']] = block['save_with_id']
    #TODO: find a better way to handle our html auto insertion...
    save_dict['html'] = ContentType.objects.get_for_model(CogComHTMLTrial).pk
    request.session['data_mapping'] = json.dumps(save_dict)
    #adding static resources to settings
    final_settings['resources'] = exp.list_static_url()
    # Good luck :)
    return JsonResponse(final_settings)

def serve_snippet(request, exp_label, template):
    prefix = 'djexperiments/'+exp_label+'/'
    return render(request, prefix+template)
    