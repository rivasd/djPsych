from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404
from django.conf import settings
import glob
import os.path
from djexperiments.models import Experiment

# Create your views here.
def lobby(request, exp_label):
    exp = get_object_or_404(Experiment, label=exp_label)
    if exp.is_active:
        template_name = 'djexperiments/'+exp_label+'/index.html'
        return render(request, template_name, )
    else:
        return Http404

@login_required
def launch(request, exp_label):
    exp = Experiment.objects.get(label=exp_label)
    js_modules = [os.path.basename(file) for file in glob.glob('./djexperiments/static/djexperiments/'+exp_label+'/*.js')]
    consentfile = 'djexperiments/'+exp_label+'/consent.html'
    plugins = [os.path.basename(file) for file in glob.glob('./djmanager/static/jspsych-plugins/*.js')]
    return render(request, 'djexperiments/launch.html', {'scripts': js_modules, 'exp': exp, 
                                                         'consent':consentfile, 'plugins':plugins, 'static_url': settings.STATIC_URL})

def summary(request, exp_label):
    return HttpResponse()
