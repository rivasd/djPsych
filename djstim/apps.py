from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_

class DjstimConfig(AppConfig):
    name = 'djstim'
    verbose_name = l_("Stimuli")
