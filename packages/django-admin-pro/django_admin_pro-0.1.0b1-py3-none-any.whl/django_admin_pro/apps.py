from django.apps import AppConfig


class DjangoAdminProConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_admin_pro"

    def ready(self):
        print("django admin pro is ready")
