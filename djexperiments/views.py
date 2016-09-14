from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings
import glob
import os.path
from djexperiments.models import Experiment
from django.utils.translation import ugettext as _
from djPsych.utils import get_all_js_files_in_exp
from django.contrib.auth.models import Group
from djexperiments.forms import SandboxForm, UploadForm
from djcollect.models import Participation
import os
from argparse import Action
from django.core.files import File
from test.test_socket import FileObjectClassTestCase
from django.core.files.storage import default_storage
from django.contrib import messages

# Create your views here.
def lobby(request, exp_label):
    try:
        exp = get_object_or_404(Experiment, label=exp_label)
    except:
        raise Http404(_("No such experiment"))
    
    if hasattr(exp, 'lobby'):
        lobby = exp.lobby.render()
    else:
        lobby = _("No homepage description available for this experiment")
    if exp.research_group not in request.user.groups.all():
        researcher = False
    else:
        researcher = True
    
    return render(request, 'djexperiments/lobby.html', {'exp': exp, 'researcher':researcher, 'lobby':lobby})
        

@login_required
def launch(request, exp_label):
    exp = Experiment.objects.get(label=exp_label)
    js_modules = get_all_js_files_in_exp(exp_label=exp_label)
    consentfile = 'djexperiments/'+exp_label+'/consent.html'
    plugins = [os.path.basename(file) for file in glob.glob(os.path.join(os.path.dirname(__file__), '../djmanager/static/jspsych-plugins/')+'*.js')]
    return render(request, 'djexperiments/launch.html', {'scripts': js_modules, 'exp': exp, 
                                                         'consent':consentfile, 'plugins':plugins, 'static_url': settings.STATIC_URL})

def summary(request, exp_label):
    return HttpResponse()

@login_required
def sandbox(request, exp_label):
    
    exp = Experiment.objects.get(label=exp_label)
    
    if not exp.research_group in request.user.groups.all():
        raise Http404(_("You do not have permission to access the sandbox"))
    
    plugins = [os.path.basename(file) for file in glob.glob(os.path.join(os.path.dirname(__file__), '../djmanager/static/jspsych-plugins/')+'*.js')]
    js_modules = get_all_js_files_in_exp(exp_label)
    configs = exp.get_all_configurations()
    choices = []
    for config in configs:
        choices.append((config.name, config.__str__()))
        
    sandboxform = SandboxForm(versions=choices)
    context= {
        'scripts': js_modules,
        'exp': exp,
        'plugins': plugins,
        'static_url': settings.STATIC_URL,
        'sandboxform': sandboxform,
        'sandbox': True,
        'version': 'test'
    }
    
    return render(request, 'djexperiments/launch.html', context)
    pass
    
@login_required
def debrief(request, exp_label):
    
    exp = Experiment.objects.prefetch_related('participation_set', 'debrief').get(label=exp_label)
    if exp.participation_set.filter(subject=request.user.subject, complete=True).exists(): # TODO: allow more refined test than: if at least one complete part
        done=True
        
    elif exp.research_group in request.user.groups.all():
        done=True
    else:
        done=False
    
    return render(request, 'djexperiments/debrief.html', {'debrief': exp.debrief.render(), 'done':done, 'explabel': exp_label})
    
@login_required
def upload_resource(request, exp_label):
    
    exp = Experiment.objects.get(label=exp_label)
    
    if not exp.research_group in request.user.groups.all():
        raise Http404(_("You do not have access to this experiment"))
    
    if 'POST' == request.method: #yoda!
          
        form = UploadForm(request.POST, request.FILES)
        filesList = request.FILES.lists()
        
        if form.is_valid():
            
            for currentFile in filesList:
                
                fileKeyValue = currentFile[0]
                actualCurrentFile = currentFile[1][0]
                    
                fileObject = File(actualCurrentFile)
                    
                initialPath = fileObject.name
                fileObject.name = "/"+exp_label+"/"+fileObject.name
                newPath = settings.MEDIA_ROOT + fileObject.name
                    
                default_storage.save(newPath, fileObject)
                    
                messages.add_message(request, messages.SUCCESS, _('Your file successfully uploaded'))
                     
                return HttpResponseRedirect("/webexp/"+exp_label+"/upload")
        
        else :
            messages.add_message(request, messages.WARNING, _('The type of your file is not valid...'))
            return HttpResponseRedirect("/webexp/"+exp_label+"/upload")
            
    else:
        form = UploadForm()
        return render(request, 'djexperiments/upload.html', {'form': form})
    
    