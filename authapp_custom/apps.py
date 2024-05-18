from django.apps import AppConfig


class AuthappCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp_custom'

    def ready(self):
        import authapp_custom.signals
