"""
views.py for djreceive app
"""

from django.shortcuts import render
from django.http import Http404
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from djPsych.exceptions import InvalidData, PayoutException
from djpay.models import Payment
import json
from djexperiments.models import Experiment
from .utils import sort_trials
import datetime
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def save(request, exp_label):
    if not request.is_ajax():
        # raise HttpResponseBadRequest
        pass
    
    if not request.user.is_authenticated():
        return JsonResponse({'error': _("You must be logged in to submit data. Refused.")})
    
    if not 'exp_id' in request.session or not 'current_exp' in request.session:
        return JsonResponse({'error':_("Data received unexpectedly. Refused.")})
    
    try:
        meta = json.loads(request.POST['meta'])
        data = json.loads(request.POST['data'])
        subject_id = meta['subject']
        previous = meta['previous']
        finished = meta['completed']
        setting_name = meta['name']
        browser_info = meta['browser']
        code = meta['exp_id']
        exp_name = meta['current_exp']
    except KeyError:
        return JsonResponse({'error':_("Invalid data format or missing obligatory metadata attributes. Refused.")})
    except ValueError:
        return JsonResponse({'error':_("Data was malformed, expecting two POST variable, each a correct JSON string. Refused")})
    
    if request.session['exp_id'] != code or request.session['current_exp'] != exp_name:
        return JsonResponse({'error':_("Data does not match last requested experiment. Did you start multiple experiments at the same time?")})
    if subject_id != request.user.subject.id:
        return JsonResponse({'error':_("The experimental data does not match your credentials. Refused.")})
    
    exp = Experiment.objects.get(label=exp_label)
    if previous == False:
        participation = exp.create_participation(subject=request.user.subject, started=request.session['start_time'], complete=finished)
    else:
        participation = exp.participation_model.objects.get(pk=previous)
    
    # now that we have the participation, create the run representing the data just received
    new_run = participation.create_run(request.session['start_time'], datetime.datetime.now(), browser_info) 
    
    try:
        mapping = json.loads(request.session['data_mapping'])
    except AttributeError:
        return JsonResponse({'error':_("A mapping between types and trial models was not specified before the experiment was sent. Cannot save.")})
    
    sortings = sort_trials(data)
    for trial_type, trial_batch in sortings.items():
        try:
            trial_content_type = ContentType.objects.get(pk=mapping[trial_type])
            trial_model = trial_content_type.model_class()
        except:
            return JsonResponse({'error': _('We could not handle your trial of type: ')+trial_type})
        instances=[]
        for trial in trial_batch:
            trial['run'] = new_run
            trial = new_run.pre_process_data(trial, request) # hook to preprocess the data
            try:
                instance = trial_model.create_from_raw_data(trial) #DONE: write the post_init signal to handle unexpected arguments
            except Exception as e:
                raise e  # for debuggin purposes
                del trial['run']
                return JsonResponse({'error':_('Could not create a trial of type ')+ trial_type+ _(' with this data: ')+ json.dumps(trial) + '\n\n'+ str(e)})
            instances.append(instance)
        
        new_run.used_trials.add(trial_content_type)
        trial_model.objects.bulk_create(instances)
    
    # By this time the saving should have been done, payments?
    message="\n"
    if exp.compensated and participation.complete and not request.user.groups.filter(name=exp.research_group.name).exists(): # prevents researchers from being paid for doing their own experiment
        try:
            payment = participation.create_payment(data)
            message = _("You have earned a payment of %f.2 %s. Go to your profile page to claim it!") % (round(payment.amount, 2), payment.currency)
        except PayoutException as e:
            message= _("However payment will not be issued because of the following reason: ")+str(e)
    
    # dont forget to save stuff
    if finished:
        participation.complete = finished
        participation.finished = datetime.datetime.now()
    participation.save()
    new_run.save()
    
    request.session['lastCompleted'] = exp.label # just so that we can give a message on the next visit
    del request.session['exp_id']       # Puts this use back in a state where he is not waiting for data
    del request.session['current_exp']  #   
    # just to test
    return JsonResponse({'success':_("Your data has been recorded successfully, thank you very much!\n")+message})
