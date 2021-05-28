from django.apps import AppConfig


class UserprofilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userProfiles'

    def ready(self):
        from . import signals