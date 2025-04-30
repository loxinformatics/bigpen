from django.apps import AppConfig

PROTECTED_GROUPS = {"ADMIN": "ADMIN", "STANDARD": "STANDARD"}
PROTECTED_GROUP_IDS = {"ADMIN": 101, "STANDARD": 102}


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app._auth"
    verbose_name = "Authentication and Authorization"
