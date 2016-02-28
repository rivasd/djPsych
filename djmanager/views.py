from django.shortcuts import render
from djexperiments.models import Experiment

# Create your views here.

def home(request):
    """
    The home page of the web experiments section
    """
    
    available = Experiment.objects.all()
    return render(request, 'homepage.html', {'manips': available})
    
    
def index(request):
    return render(request, 'index.html')