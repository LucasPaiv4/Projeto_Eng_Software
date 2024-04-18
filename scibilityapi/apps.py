from django.apps import AppConfig


class ScibilityapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scibilityapi'
    
    def ready(self):
        import scibilityapi.signals