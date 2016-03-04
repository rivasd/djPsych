from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from djuser.models import Subject
from django.http.response import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_
from djcollect.models import Participation
from djuser.utils import get_my_exps
from djuser.forms import SubjectForm, PublicUserForm
from django.core.urlresolvers import reverse
# Create your views here.

@login_required
def show_profile(request):
    """
    Returns a detailed profile page for the logged-in user, with a ModelForm that allows to set some account details
    
    Uses a template that lives in djuser/templates/djuser/profile.html
    We should take advantage of Django's built-in ModelForm capabilities, which creates and manages HTML forms linked to model instances
    see: https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/#modelform
    """
    

        
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST, instance=request.user.subject)
        user_form = PublicUserForm(request.POST, instance=request.user)
        
        if subject_form.is_valid() and user_form.is_valid():
            subject_form.save()
            user_form.save()
            return HttpResponseRedirect(reverse("webexp:profiles:personal"))
        
    else:
        subject = request.user.subject
        subject_form = SubjectForm(instance=subject)
        public_user_form = PublicUserForm(instance=subject.user)
        
    participations = Participation.objects.prefetch_related('run_set', 'payment', 'experiment').filter(subject__user=request.user)
    researchs = get_my_exps(request.user)
    payments = []
    for part in participations:
        if hasattr(part, 'payment') and not part.payment.sent:
            payments.append(part.payment)
    context = {
        'participations': participations,
        'subject'       : subject,
        'payments'      : payments,
        'researchs'     : researchs,
        'subjectform'   : subject_form,
        'userform'      : public_user_form
        
    }
    
    return render(request, 'djuser/profile.html', context=context)
    
    pass