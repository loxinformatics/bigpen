import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"

    def ready(self):
        try:
            from apps.core.config.navigation import header_nav_config, aside_nav_config
            from apps.core.config.urls import urls_config

            # Configure landing url
            urls_config.register_landing_url("landing", f"{self.name}")

            # nav items
            header_nav_config.register(
                name="Home",
                url_name="landing",
                fragment="hero",
                order=0,
                icon="bi bi-house",
            )
            header_nav_config.register(
                name="Contact",
                url_name="landing",
                fragment="contact",
                order=3,
                icon="bi bi-envelope",
            )

            # nav items
            aside_nav_config.register(
                name="Home",
                url_name="landing",
                fragment="hero",
                order=0,
                icon="bi bi-house",
            )
            aside_nav_config.register(
                name="Contact",
                url_name="landing",
                fragment="contact",
                order=3,
                icon="bi bi-envelope",
            )
        except Exception as e:
            logger.warning(f"Failed to configure core app settings: {e}")
