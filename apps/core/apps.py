from django.apps import AppConfig

APP_NAME = "apps.core"


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP_NAME
