from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_

class DjcollectConfig(AppConfig):
    name = 'djcollect'
    verbose_name = l_("Data manipulation & transfer")