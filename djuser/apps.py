from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_

class DjuserConfig(AppConfig):
    name = 'djuser'
    verbose_name = l_("Subjects and User info models")
    def ready(self):
        import djuser.handlers