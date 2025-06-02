from importlib import import_module

from django.apps import AppConfig


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core.landing"

    def ready(self):
        import_module(f"{self.name}.navigation")
