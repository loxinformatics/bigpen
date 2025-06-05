from importlib import import_module

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core.authentication"

    def ready(self):
        # Import nav_registry to ensure they are registered
        try:
            import_module(f"{self.name}.nav_registry")
        except ImportError as e:
            print(f"Error importing nav_registry: {e}")
