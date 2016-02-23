from django.apps import AppConfig



class DjexperimentsConfig(AppConfig):
    name = 'djexperiments'
    
    def ready(self):
        import djexperiments.handlers  # @UnresolvedImport