import logging
from importlib import import_module

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        try:
            # Import signals to ensure they are registered
            import_module(f"{self.name}.signals")

        except Exception as e:
            logger.warning(f"Failed to configure core app settings: {e}")
