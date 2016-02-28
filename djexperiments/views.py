from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
import glob
import os.path
from djexperiments.models import Experiment

# Create your views here.
def lobby(request, exp_label):
    template_name = 'djexperiments/'+exp_label+'/index.html'
    return render(request, template_name, )

@login_required
def launch(request, exp_label):
    exp = Experiment.objects.get(label=exp_label)
    js_modules = [os.path.basename(file) for file in glob.glob('./djexperiments/static/djexperiments/'+exp_label+'/*.js')]
    consentfile = 'djexperiments/'+exp_label+'/consent.html'
    plugins = [os.path.basename(file) for file in glob.glob('./djmanager/static/jspsych-plugins/*.js')]
    return render(request, 'djexperiments/launch.html', {'scripts': js_modules, 'exp': exp, 'consent':consentfile, 'plugins':plugins})

def summary(request, exp_label):
    return HttpResponse()
