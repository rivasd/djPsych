from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_

class DjpayConfig(AppConfig):
    name = 'djpay'
    verbose_name= l_("Payment & remuneration models")
