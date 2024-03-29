from django.apps import AppConfig

class B26Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b26'

    def ready(self):
        import b26.signals