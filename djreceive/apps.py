from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_


class DjreceiveConfig(AppConfig):
    name = 'djreceive'
    verbose_name= l_("Experimental data models")