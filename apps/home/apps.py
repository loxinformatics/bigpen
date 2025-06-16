import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"

    def ready(self):
        try:
            from apps.core.config.navigation import nav_config
            from apps.core.config.urls import landing_url_config

            # Configure landing url
            landing_url_config.register_landing_url("landing", f"{self.name}")

            # Add landing url to nav items
            nav_config.register("Home", "landing", fragment="hero", order=0)
            nav_config.register("Contact", "landing", fragment="contact", order=3)
        except Exception as e:
            logger.warning(f"Failed to configure core app settings: {e}")
