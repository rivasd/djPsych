from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_

class DjsendConfig(AppConfig):
    name = 'djsend'
    verbose_name = l_("Experimental settings models")
    def ready(self):
        pass
