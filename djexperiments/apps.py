from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as l_


class DjexperimentsConfig(AppConfig):
    name = 'djexperiments'
    verbose_name = l_("Experiment administration")
    def ready(self):
        import djexperiments.handlers  # @UnresolvedImport