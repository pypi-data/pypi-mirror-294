from django.apps import AppConfig
from django.conf import settings


class DjangoAdminProConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_admin_pro"

    def ready(self):
        django_breeze_app = "django_breeze"

        if django_breeze_app not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (django_breeze_app,)
