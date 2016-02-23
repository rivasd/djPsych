from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

# Create your views here.
def lobby(request, exp_label):
    template_name = 'djexperiments/'+exp_label+'/index.html'
    return render(request, template_name, )

@login_required
def launch(request, exp_label):
    template = 'djexperiments/'+exp_label+'/consent.html'
    return render(request, template)

def summary(request, exp_label):
    return HttpResponse()
