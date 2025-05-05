from importlib import import_module

from django.apps import AppConfig

PROTECTED_GROUPS = {"ADMIN": "ADMIN", "STANDARD": "STANDARD"}
PROTECTED_GROUP_IDS = {"ADMIN": 101, "STANDARD": 102}


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app._auth"
    verbose_name = "Authentication and Authorization"

    def ready(self):
        import_module(f"{self.name}.signals")
