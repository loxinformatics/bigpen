import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

APP_NAME = "apps.custom"


class CustomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP_NAME

    def ready(self):
        try:
            from apps.core.management.config.auth import auth_config
            from apps.core.management.config.navigation import nav_config
            from apps.core.management.config.urls import urls_config

            # Configure landing url
            urls_config.register_landing_url("landing", self.name)

            # Disable auth pages
            # auth_config.disable_page("signup")
            # auth_config.disable_page("signin")

            # Configure page settings (no role management needed)
            auth_config.configure_username_field(
                label="Phone Number",
                placeholder="Enter your Phone Number (with country code e.g. +254700000000)",
            )

            # nav items
            nav_config.register(
                name="Home",
                url_name="landing",
                fragment="hero",
                order=0,
                icon="bi bi-house",
            )
            nav_config.register(
                name="Products",
                url_name="portfolio",
                order=2,
                icon="bi bi-grid",
            )
            nav_config.register(
                name="Features",
                url_name="features",
                order=3,
                icon="bi-tags",
            )
            nav_config.register(
                name="Contact",
                url_name="contact",
                order=5,
                icon="bi bi-envelope",
            )

            logger.info(f"{self.name} configured successfully")

        except Exception as e:
            logger.warning(f"Failed to configure {self.name} config: {e}")
