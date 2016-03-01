from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from .models import Payment
from djPsych.exceptions import PayoutException

# Create your views here.

def claim(request, exp_label, code):
    """
    Another JSON view, this one used to execute payment
    """
    
    error=""
    try:
        payment = Payment.objects.get(pk=code)
        try:
            payment.pay(request)
        except PayoutException as e:
            error =_("Payment delivery failed: ")+str(e)
    except Payment.DoesNotExist:
        payment = None
        error = _("Invalid payment code")
    
    if request.is_ajax():
        if error != "":
            return JsonResponse({'error':error})
        else:
            return JsonResponse({'success': _("Yay! Payment successfully sent to: ")+payment.receiver})
    else:
        return render(request, 'payout.html', {'error': error, 'payment': payment})
    pass