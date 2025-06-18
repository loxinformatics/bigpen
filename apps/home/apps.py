import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"

    def ready(self):
        try:
            from apps.core.management.config.navigation import nav_config
            from apps.core.management.config.urls import urls_config

            # Configure landing url
            urls_config.register_landing_url("landing", self.name)

            # nav items
            nav_config.register(
                name="Home",
                url_name="landing",
                fragment="hero",
                order=0,
                icon="bi bi-house",
                auth_status="public",
            )
            nav_config.register(
                name="Contact",
                url_name="landing",
                fragment="contact",
                order=3,
                icon="bi bi-envelope",
                auth_status="public",
            )

        except Exception as e:
            logger.warning(f"Failed to configure core app settings: {e}")
