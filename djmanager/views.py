from django.shortcuts import render
from djexperiments.models import Experiment
import glob
import os.path
# Create your views here.

def home(request):
    """
    The home page of the web experiments section
    """
    plugins = [os.path.basename(file) for file in glob.glob('./djmanager/static/jspsych-plugins/*.js')]
    available = Experiment.objects.all()
    return render(request, 'homepage.html', {'manips': available, 'plugins': plugins})
    
def allExperiments(request):
    return render(request, 'allExperiments.html')

    
def index(request):
    return render(request, 'index.html')