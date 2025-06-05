from importlib import import_module

from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.base"
    verbose_name = "Organization (Base)"

    def ready(self):
        # Import signals to ensure they are registered
        try:
            import_module(f"{self.name}.signals")
        except ImportError as e:
            print(f"Error importing signals: {e}")
