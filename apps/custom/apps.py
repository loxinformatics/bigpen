import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CustomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.custom"
    verbose_name = "Functional Modules"

    def ready(self):
        try:
            # Only configure non-role related auth settings
            from apps.core.config.auth import auth_config

            # Configure page settings (no role management needed)
            auth_config.configure_username_field(
                label="Phone Number", placeholder="Enter your Phone Number (with country code e.g. +254700000000)"
            )

            logger.info("BigPen app configured successfully")

        except Exception as e:
            logger.warning(f"Failed to configure BigPen app settings: {e}")
