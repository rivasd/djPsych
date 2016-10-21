from django.shortcuts import render
from djexperiments.models import Experiment
from djPsych.utils import fetch_files_of_type
# Create your views here.

def home(request):
    """
    The home page of the web experiments section
    """

    available = Experiment.objects.all()
    return render(request, 'homepage.html', {'manips': available})
    
def allExperiments(request):
    return render(request, 'allExperiments.html')

    
def index(request):
    return render(request, 'index.html')