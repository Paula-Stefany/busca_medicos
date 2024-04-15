from django.apps import AppConfig


class MedicsearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medicSearch'

    def ready(self): 
        import medicSearch.signals
