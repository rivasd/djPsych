from django.apps import AppConfig


class DjuserConfig(AppConfig):
    name = 'djuser'
    def ready(self):
        import djuser.handlers