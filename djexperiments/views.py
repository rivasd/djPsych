from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404, HttpResponseRedirect, JsonResponse,HttpResponseBadRequest
from django.conf import settings
from django.core.files.storage import default_storage
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
from django.contrib import messages
from djmanager.utils import get_allowed_exp_for_user
from djPsych.utils import fetch_files_of_type, get_type
import json

# Create your views here.
def lobby(request, exp_label):
    try:
        exp = Experiment.objects.prefetch_related("research_group__user_set").get(label =exp_label)
    except Experiment.DoesNotExist as E:
        raise Http404(_("No such experiment"))
    
    if not exp.is_researcher(request):
    
        if  hasattr(exp, 'lobby'):
            lobby = exp.lobby.render()
        else:
            lobby = _("No homepage description available for this experiment")
        return render(request, 'djexperiments/lobby.html', {'exp': exp, 'lobby':lobby})
    else: 
        uploadForm = UploadForm()
        researcher_experiments = Experiment.objects.filter(research_group__in = request.user.groups.all())
        return render(request, 'djexperiments/control_panel.html', {'exp': exp, 'researcher_experiments' : researcher_experiments, 'listdir': exp.list_static_resources(), 'uploadForm':uploadForm})  

@login_required
def launch(request, exp_label):
    exp = Experiment.objects.get(label=exp_label)
    
    resources = exp.list_static_urls()
    if os.path.exists(os.path.join(settings.BASE_DIR, "..", 'djexperiments', "templates", 'djexperiments', exp.label, 'consent.html')):
        consentfile = 'djexperiments/'+exp_label+'/consent.html'
    else:
        consentfile = None
    
    plugins = fetch_files_of_type('djPsych/jsPsych/plugins', 'js')
    
    completion = {}
    #check if completion of a specific participation was requested
    if request.GET.get("continue", default=None):
        request.session["continue"] = request.GET['continue']
        completion = Participation.objects.get(pk=request.session['continue']).completion_status()
    else:
        latest = exp.get_latest_pending(request)
        completion = latest.completion_status() if latest else {}
    #send a brief description of the requested participation (if any), or the last one, or nothing if this is the very first time
    
    
    
    return render(request, 'djexperiments/launch.html', {'resources': resources, 'exp': exp, 'completion':json.dumps(completion), 'sandbox': False,
                                                         'consent':consentfile, 'plugins':plugins, 'static_url': settings.STATIC_URL, 'header_type': 'mdl-layout__header--scroll'})

def summary(request, exp_label):
    return HttpResponse()

@login_required
def sandbox(request, exp_label):
    
    exp = Experiment.objects.get(label=exp_label)
    
    if not exp.research_group in request.user.groups.all():
        raise Http404(_("You do not have permission to access the sandbox"))
    
    plugins = fetch_files_of_type('djPsych/jsPsych/plugins', 'js')
    resources = exp.list_static_urls()
    configs = exp.get_all_configurations()
    choices = []
    for config in configs:
        choices.append((config.name, config.__str__()))
        
    sandboxform = SandboxForm(versions=choices)
    context= {
        'resources': resources,
        'exp': exp,
        'plugins': plugins,
        'static_url': settings.STATIC_URL,
        'sandboxform': sandboxform,
        'sandbox': True,
        'version': 'test',
        'completion': json.dumps({})
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
        filesList = request.FILES.getlist('file')
        
        if form.is_valid():
            
            for currentFile in filesList:
                
                    
                fileObject = File(currentFile)
                    
                initialPath = fileObject.name
                fileObject.name = "/"+exp_label+"/"+fileObject.name
                newPath = settings.MEDIA_ROOT + fileObject.name
                    
                default_storage.save(newPath, fileObject)
                    
                messages.add_message(request, messages.SUCCESS, _('Your file successfully uploaded: ')+initialPath)
                
            return HttpResponseRedirect("/webexp/"+exp_label+"/upload")   
        
        else :
            messages.add_message(request, messages.WARNING, _('The type of your file is not valid...'))
            return HttpResponseRedirect("/webexp/"+exp_label+"/upload")
            
    else:
        form = UploadForm()
        return render(request, 'djexperiments/upload.html', {'form': form})
    
@login_required
def exp_filesystem(request, exp_label):
    """
    Single RESTful view to interact with the personal file tree of an experiment
    """
    try:
        exp = Experiment.objects.get(label=exp_label)
    except Experiment.DoesNotExist:
        return JsonResponse({'error': _("There is no experiment by the name: "+exp_label)})
    
    if not exp.is_researcher(request):
        return JsonResponse({'error': _("You are not authorized to browse: "+exp_label)})
    
    #Reject all GET request so we can simplify the interface
    if request.method == "POST":
        if request.POST["action"] == "ls":
            #request to get full directory desription, in jsTree-readable format
            contents = exp.list_static_resources()
            response = contents
            
            if request.POST["mode"] == "jsTree":
                response = [{"text": exp.label, "type":'#', "icon":"fa fa-folder", "data":exp.label, "state":{"opened":True}}]
                root_nodes = []
                
                for folder, files in contents.items():
                    
                    if folder == "root":
                        target = root_nodes
                    else:
                        folder_node = {
                            "text":folder, 
                            "type":"folder", 
                            "data":exp.label+'/'+folder, 
                            "children":[]
                        }
                        root_nodes.append(folder_node)
                        target = folder_node['children']
                        
                    for file in files:
                        subfolder = (folder+'/') if folder != "root" else ""
                        file_node={
                            "data":exp.label+'/'+subfolder+file,
                            "type": get_type(file),
                            "text": file
                        }
                        target.append(file_node)

                response[0]["children"] = root_nodes
            
            return JsonResponse(response, safe=False)
        
        elif request.POST["action"] == "rm":
            to_delete = json.loads(request.POST["args"])
            #some checks across all paths to delete
            for filename in to_delete:
                full_path = default_storage.path(os.path.join(filename))
                if not os.path.exists(full_path):
                    return JsonResponse({'error':_("requested file :"+filename+" does not exist")})
                if os.path.isdir(full_path):
                    return JsonResponse({'error':_("cannot delete folders")})
            #if no errors, actually delete
            for filename in to_delete:   
                default_storage.delete(filename)

            return JsonResponse({'success':True})
        
        elif request.POST["action"] == "mkdir":
            parentDir = request.POST["parent"]
            name = request.POST["name"]
            
            try:
                os.mkdirs(os.path.join(default_storage.location, exp.label, parentDir, name), exist_ok = True) #@UndefinedVariable
            except OSError as e:
                return JsonResponse({"error":str(e)})
            return JsonResponse({'success': True, 'nodes':[{"text":name, "type":"folder"}]})
        
        elif request.POST["action"] == "add":
            filesList = request.FILES.getlist('uploads')
            parentDir = request.POST["parent"]
            newNodes = []
            for currentFile in filesList:
                fileObject = File(currentFile)
                initialPath = fileObject.name
                newPath = os.path.join(default_storage.location, exp.label, parentDir, initialPath)
                relative_path = os.path.join(exp.label, parentDir, initialPath)
                default_storage.save(newPath, fileObject)
                messages.add_message(request, messages.SUCCESS, _('Your file successfully uploaded: ')+initialPath)
                
                newNodes.append({"text": initialPath, "data":relative_path, "type":get_type(initialPath)})
            
            return JsonResponse({"success":True, "nodes":newNodes})
        
        elif request.POST["action"] == "rename":
            
            return JsonResponse()
            
    else:
        return JsonResponse({'error': _("This API only available through POST request"+exp_label)})
    